"""
    OscapReports:
        Handle the parsing of .xml reports, performs summaries and compares them
"""

import logging
import xml.etree.ElementTree as et

class OscapReports(object):
    """ Handles the parsing of .xml reports  """

    def parse_xml(self, xml_report):
        """ Function to summarize a report by saving general data """

        tree = et.parse(xml_report)
        root = tree.getroot()

        # Namespace used by the ssg-ol8-xccdf.xml format
        ns = {
            'default': 'http://checklists.nist.gov/xccdf/1.2'
        }

        test_results = root.findall('.//default:TestResult/*', namespaces=ns)
        result_root = et.Element('TestResult', namespaces=ns)

        for element in test_results:
            if element.tag == '{http://checklists.nist.gov/xccdf/1.2}rule-result':
                result_element = element.find('default:result', namespaces=ns)
                if result_element is not None and 'notselected' in result_element.text:
                    continue
            result_root.append(element)

        result_tree = et.ElementTree(result_root)
        result_tree.write(xml_report, encoding='utf-8', xml_declaration=True)

    def get_summary(self, xml_report, id_report):
        """ Function to retrieve general report data """

        tree = et.parse(xml_report)
        root = tree.getroot()

        # Namespace used by the ssg-ol8-xccdf.xml format
        ns = {
            'default': 'http://checklists.nist.gov/xccdf/1.2'
        }

        # Dictionary to store summarized scan data
        summary = {}
        # List to store detailed scan results data
        detailed_results = []

        # Dictionary used to store overall scan results
        overall_results = {
            'Passed' : 0,
            'Failed' : 0,
            'Score' : 0
        }

        title = root.find('default:title', namespaces=ns).text
        identity = root.find('default:identity', namespaces=ns).text
        score = float(root.find('default:score', namespaces=ns).text)
        profile = root.find('default:profile', namespaces=ns).attrib['idref']
        
        for rule_result in root.findall('default:rule-result', namespaces=ns):
            rule = rule_result.attrib.get('idref')
            result = rule_result.find('./default:result', namespaces=ns)

            test_summary = {
                'Rule' : rule,
                'Result' : result.text
            }

            # Fill the ovarall results with the results for each checked rule
            if result.text == 'pass':
                overall_results['Passed'] += 1
            elif result.text == 'fail':
                overall_results['Failed'] += 1

            overall_results['Score'] = f'{score:.2f}%'
            detailed_results.append(test_summary)

        summary['idx'] = id_report
        summary['title'] = title
        summary['identity'] = identity
        summary['profile'] = profile
        summary['timestamp'] = xml_report.split('/')[-1].split('.')[0]

        return summary, overall_results, detailed_results

    def print_report(self, summary, results):
        """ Function to print a scan report in a cool way """

        len_header = len(summary['title']) + 8
        print("=" * len_header)
        print(f"=== {summary['title']} ===")
        print("=" * len_header + "\n")

        print(f"This report was generetad by {summary['identity']} on {summary['timestamp']} following the {summary['profile']} profile\n")

        for idx, result in enumerate(results, start=1):
            print(f"================== Test Results {idx} ==================")
            for key, value in result.items():
                print(f"{key}: {value}")
            print("======================================================")

    def compare_results(self, results1, results2):
        """ Function to get the main differences between the results of two reports """

        differences = []
        dict1_map = {d['Rule']: d for d in results1}
        dict2_map = {d['Rule']: d for d in results2}

        # Compare results1 with results2
        for rule, dict1 in dict1_map.items():
            dict2 = dict2_map.get(rule)
            if dict2:
                if dict1['Result'] != dict2['Result']:
                    diff_dict = {
                        'rule': rule,
                        'list1_value': dict1['Result'],
                        'list2_value': dict2['Result']
                    }
                    differences.append(diff_dict)
            else:
                diff_dict = {
                    'rule': rule,
                    'list1_value': dict1['Result'],
                    'list2_value': 'notfound'
                }
                differences.append(diff_dict)

        # Compare results2 with results1
        for rule, dict2 in dict2_map.items():
            # Exclude repeated differences
            if rule not in dict1_map:
                diff_dict = {
                    'rule': rule,
                    'list1_value': 'notfound',
                    'list2_value': dict2['Result']
                }
                differences.append(diff_dict)

        return differences

    def print_differences(self, overall1, overall2, differences):
        """ Function to print the differences of to scan reports in a cool way """

        if not differences:
            return "No differences found"

        self.print_overall(overall1, overall2)

        output = "\n"
        for idx, diff_dict in enumerate(differences, start=1):
            output += f"  Difference {idx}:\n"
             
            rule = diff_dict['rule']
            list1_value = diff_dict['list1_value']
            list2_value = diff_dict['list2_value']
            output += f"    Rule: {rule}\n"
            output += f"    Result: {list1_value} -> {list2_value}\n"

        print(output)

    def print_overall(self, overall1, overall2):
        """ Function to print the general data of a couple of scan report """

        all_keys = set(list(overall1.keys()) + list(overall2.keys()))

        max_key_length = max(len(key) for key in all_keys)
        max_value_length = max(len(str(val)) for val in list(overall1.values()) + list(overall2.values()))

        header = f"| {'Results':<{max_key_length + 2}} | {'First':<{max_value_length}} | {'Second':<{max_value_length}} |"

        separator = f"+{'-' * (max_key_length + 4)}+{'-' * (max_value_length + 4)}+{'-' * (max_value_length + 5)}+"

        print('\n' + separator)
        print(header)
        print(separator)

        for key in all_keys:
            val1 = overall1.get(key, "-")
            val2 = overall2.get(key, "-")
            row = f"| {key:<{max_key_length + 2}} | {str(val1):<{max_value_length + 2}} | {str(val2):<{max_value_length + 3}} |"
            print(row)

        print(separator)
