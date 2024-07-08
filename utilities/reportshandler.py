import xml.etree.ElementTree as et

class OscapReports(object):
    def parse_xml(self, xml_report, id_report):
        tree = et.parse(xml_report)
        root = tree.getroot()

        summary = {}
        detailed_results = []

        overall_results = {
            'Passed' : 0,
            'Failed' : 0,
            'NotApplicable' : 0
        }

        ns = {
            'default': 'http://checklists.nist.gov/xccdf/1.2'
        }

        title = root.find('.//default:title', namespaces=ns)
        description = root.find('.//default:description', namespaces=ns)
        test_result = root.find('.//default:TestResult', namespaces=ns)

        if test_result is not None:
            identity = test_result.find('./default:identity', namespaces=ns)
            profile_tag = test_result.find('./default:profile', namespaces=ns)

            if profile_tag is not None:
                profile = profile_tag.attrib.get('idref')

            for rule_result in test_result.findall('./default:rule-result', namespaces=ns):
                rule = rule_result.attrib.get('idref')
                severity = rule_result.attrib.get('severity')
                result = rule_result.find('./default:result', namespaces=ns)

                test_summary = {
                    'Rule' : rule,
                    'Severity' : severity,
                    'Result' : result.text
                }

                if result.text == 'pass':
                    overall_results['Passed'] += 1
                elif result.text == 'fail':
                    overall_results['Failed'] += 1
                else:
                    overall_results['NotApplicable'] += 1

                detailed_results.append(test_summary)

        timestamp = test_result.attrib.get('start-time')

        summary['idx'] = id_report
        summary['title'] = title.text
        summary['description'] = description.text
        summary['identity'] = identity.text
        summary['profile'] = profile
        summary['timestamp'] = timestamp

        return summary, overall_results, detailed_results

    def print_report(self, summary, results):
        len_header = len(summary['title']) + 8

        print(f"=== {summary['title']} ===\n")
        print(summary['description'])
        print(f"=" * len_header + "\n")

        print(f"This report was generetad by {summary['identity']} on {summary['timestamp']} following the {summary['profile']} profile\n")

        for idx, result in enumerate(results, start=1):
            print(f"================== Test Results {idx} ==================")
            for key, value in result.items():
                print(f"{key}: {value}")
            print("======================================================")

    def compare_reports(self, results1, results2):
        differences = []
        keys = ['Rule','Severity','Result']

        for dict1, dict2 in zip(results1, results2):
            if all(dict1[key] == dict2[key] for key in keys):
                continue
            else:
                diff_dict = {}
                for key in keys:
                    if dict1.get(key) != dict2.get(key):
                        diff_dict[key] = {
                            'rule': dict1.get('Rule'),
                            'list1_value': dict1.get(key),
                            'list2_value': dict2.get(key)
                        }
                differences.append(diff_dict)

        return differences
    
    def print_differences(self, overall1, overall2, differences):
        if not differences:
            return "No differences found"

        self.print_overall(overall1, overall2)

        output = "\n"
        for idx, diff_dict in enumerate(differences, start=1):
            output += f"  Difference {idx}:\n"
            for key, values in diff_dict.items():
                rule = values['rule']
                list1_value = values['list1_value']
                list2_value = values['list2_value']
                output += f"    Rule: {rule}\n"
                output += f"    {key} {list1_value} -> {list2_value}\n"

        print(output)

    def print_overall(self, overall1, overall2):
        all_keys = set(list(overall1.keys()) + list(overall2.keys()))

        max_key_length = max(len(key) for key in all_keys)
        max_value_length = max(len(str(val)) for val in list(overall1.values()) + list(overall2.values()))

        header = f"| {'Results':<{max_key_length + 2}} | {'First':<{max_value_length}} | {'Second':<{max_value_length}} |"
        separator = f"+{'-' * (max_key_length + 4)}+{'-' * (max_value_length + 4)}+{'-' * (max_value_length + 5)}+"
        
        print(separator)
        print(header)
        print(separator)

        for key in all_keys:
            val1 = overall1.get(key, "-")
            val2 = overall2.get(key, "-")
            row = f"| {key:<{max_key_length + 2}} | {str(val1):<{max_value_length + 2}} | {str(val2):<{max_value_length + 3}} |"
            print(row)

        print(separator)

