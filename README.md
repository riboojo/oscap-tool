# Oscap Tool
Simple command line tool for regular openscap scans of the Oracle Linux 8


| Release | Date <br> (mm-dd-yyyy) | Author       | Description     |
| :---:   | :---:                  | :---:        | :---:           |
| 1.0     | 07-08-2024             | rbojorquez   | First release: <br> All functionality covered    |
| 1.1     | 07-08-2024             | rbojorquez   | Fix duplicated instance of OscapScanner    |
| 1.2     | 07-08-2024             | rbojorquez   | Fix Pylint warnings    |
| 1.3     | 07-08-2024             | rbojorquez   | Improve the history table format    |

## Preconditions

Install the OpenSCAP tool:

```console
$ yum install openscap-scanner
```

Install the policies provided by SCAP Segurity Guide (SSG):
```console
$ yum install scap-security-guide
```

You can find the available profiles to use under ***/usr/share/xml/scap/ssg/content/***. Detailed information of profiles available by:
```console
$ oscap info /usr/share/xml/scap/ssg/content/ssg-ol8-xccdf.xml
```

## Functionality

- **Scan:** Execute oscap scan and print the report
- **History:** List history of executed scans
- **Consult:** Print a scan report by its id available from the history
- **Compare:** Compare two scan reports available from the history by its ids

This tool uses by default the ***xccdf_org.ssgproject.content_profile_stig*** profile. As well as the rules described in ***ssg-ol8-xccdf***.

## Usage

You can perform any of the existing functionality with one line command input as the following examples:

***To perform a scan***

```console
$ python3 oscaptool.py scan
```

***To check the history***

```console
$ python3 oscaptool.py history
```

***To consult the scan report with id 1***

```console
$ python3 oscaptool.py consult 1
```

***To compare the scan report with id 1 against the one with id 2***

```console
$ python3 oscaptool.py compare 1 2
```
Or you can either use the menu:

```console
$ python3 oscaptool.py
Select one of the following commands:
1: scans
2: history
3: consult
4: compare
>
```

```console
$ python3 oscaptool.py consult
Enter an ID to consult its report:
>
```
