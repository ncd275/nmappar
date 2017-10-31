import click
import re
import csv
import sys


@click.command()
@click.option('--options', default="hps", help='number of greetings')
@click.option('--function', default="null", help='number of greetings')
@click.argument('file', type=click.File('rb'))
def main(options, function, file):
    data = file.readlines()
    opts = list(options)
    if function == 'print':
        printFile(data)
    if 'live-host' in function.lower():
        printBanner(opts)
        getLiveHosts(opts, data)
    if 'dead-host' in function.lower():
        getDeadHosts(data)
    if 'search-service' in function.lower():
        terms = []
        termStr = function.split("=")[1]
        if ',' in termStr:
            terms = termStr.split(",")
        else:
            terms.append(termStr)
        printBanner(opts)
        searchServices(opts, terms, data)
    if 'uniq-service' in function.lower():
        printBanner(["p","s"])
        uniqServices(opts, data)
    if 'search-host' in function.lower():
        hosts = []
        hostStr = function.split("=")[1]
        if ',' in hostStr:
            hosts = hostStr.split(",")
        else:
            hosts.append(hostStr)
        printBanner(opts)
        searchHosts(opts, hosts, data)
    if 'search-port' in function.lower():
        portStr = function.split("=")[1]
        ports = []
        if ',' in portStr:
            ports = portStr.split(",")
        else:
            ports.append(portStr)

        printBanner(opts)
        searchPorts(opts, ports, data)
    if 'convert-csv' in function.lower():
        convert_csv(data, file.name)


def printFile(data):
    click.echo(data)


def printFunction(portsNservices, options):

        if all(o in options for o in ["h", "p", "s"]):
            for ps in portsNservices:
                click.echo("\t"+ps[0]+"\t ------ \t"+ps[1]+"\t ------ \t"+ps[2])
        elif all(o in options for o in ["h","p"]):
            for ps in portsNservices:
                click.echo("\t"+ps[0]+"\t ------ \t"+ps[1])
        elif all(o in options for o in ["h", "s"]):
            for ps in portsNservices:
                click.echo("\t"+ps[0]+"\t ------ \t"+ps[2])
        elif all(o in options for o in ["p","s"]):
            for ps in portsNservices:
                click.echo("\t"+ps[1]+"\t ------ \t"+ps[2])
        elif all(o in options for o in ["h"]):
            for ps in portsNservices:
                click.echo("\t"+ps[0])
        elif all(o in options for o in ["s"]):
            for ps in portsNservices:
                click.echo("\t"+ps[2])
        elif all(o in options for o in ["p"]):
            for ps in portsNservices:
                click.echo("\t"+ps[1])


def getLiveHosts(opts, data):
    list1 = []
    for line in data:
        if 'Host:'in line and 'Ports:' in line:

            for l in line.split("Ports: ")[1].split(", "):
                if '/open/' in l:
                    if 'Ignored State' in l:
                        pair = (line.split("Host: ")[1].split(" (")[0],re.split("/open/[^\s]*?//", l)[0],
                                re.split("/open/[^\s]*?//", l)[1].split("\tIgnored State:")[0]+"\n")
                    else:
                        pair = (line.split("Host: ")[1].split(" (")[0],re.split("/open/[^\s]*?//", l)[0],
                                re.split("/open/[^\s]*?//", l)[1])
                    list1.append(pair)
    printFunction(list1, opts)


def searchServices(opts, searchTerms, data):
    list1 = []
    for line in data:
        if 'Host:'in line and 'Ports:' in line:

            for l in line.split("Ports: ")[1].split(", "):
                if '/open/' in l:
                    if 'Ignored State' in l:
                        pair = (line.split("Host: ")[1].split(" (")[0],re.split("/open/[^\s]*?//", l)[0],
                                re.split("/open/[^\s]*?//", l)[1].split("\tIgnored State:")[0])
                    else:
                        pair = (line.split("Host: ")[1].split(" (")[0],re.split("/open/[^\s]*?//", l)[0],
                                re.split("/open/[^\s]*?//", l)[1])
                    for searchTerm in searchTerms:
                        if searchTerm.lower() in pair[2].lower():
                            list1.append(pair)
    try:
        list1.sort(key=lambda x: int(x[1]))
    except Exception as e:
        pass
    printFunction(list1, opts)


def searchHosts(opts, hosts, data):
    pair = ''
    list1 = []
    for line in data:
        if 'Host:'in line and 'Ports:' in line:

            for l in line.split("Ports: ")[1].split(", "):
                if '/open/' in l:
                    if 'Ignored State' in l:
                        pair = (line.split("Host: ")[1].split(" (")[0],re.split("/open/[^\s]*?//", l)[0],
                                re.split("/open/[^\s]*?//", l)[1].split("\tIgnored State:")[0]+"\n")
                    else:
                        pair = (line.split("Host: ")[1].split(" (")[0],re.split("/open/[^\s]*?//", l)[0],
                                re.split("/open/[^\s]*?//", l)[1])
                    for host in hosts:
                        if '*' in host:
                            pattern = host.replace(".","\.").replace("*", "(.+)")+"$"
                            compiled = re.compile(pattern)
                            if compiled.match(pair[0]):
                                list1.append(pair)
                        else:
                            if host == pair[0]:
                                list1.append(pair)

    printFunction(list1, opts)

def searchPorts(opts, ports, data):
    list1 = []
    pair = ''
    for line in data:
        if 'Host:'in line and 'Ports:' in line:

            for l in line.split("Ports: ")[1].split(", "):
                if '/open/' in l:
                    if 'Ignored State' in l:
                        pair = (line.split("Host: ")[1].split(" (")[0],re.split("/open/[^\s]*?//", l)[0],
                                re.split("/open/[^\s]*?//", l)[1].split("\tIgnored State:")[0])
                    else:
                        pair = (line.split("Host: ")[1].split(" (")[0],re.split("/open/[^\s]*?//", l)[0],
                                re.split("/open/[^\s]*?//", l)[1])

                    for port in ports:
                        if port.lower() == pair[1].lower():
                            list1.append(pair)
    try:
        list1.sort(key=lambda x: int(x[1]))
    except:
        pass
    printFunction(list1, opts)

def uniqServices(opts, data):
    all_services = []
    uniq_services = []
    uniq = []

    for line in data:
        if 'Ports: ' in line:
            for port in line.split("Ports: ")[1].split(", "):
                if 'open' in port:
                    if 'Ignored State' in port:
                        all_services.append("\t"+re.sub(r"/open/[^\s]*?//", ": --------------- \t", port)
                                            .replace("\n", "").split("\tIgnored State:")[0])
                    else:
                        all_services.append("\t"+re.sub(r"/open/[^\s]*?//", ": --------------- \t", port)
                                            .replace("\n", ""))
    uniq = set(all_services)
    for service in uniq:
        uniq_services.append(service)
    try:
        uniq_services.sort(key=lambda x: int(x.split(":")[0]))
    except Exception as e:
        pass
    for service in uniq_services:
        click.echo(service)


def getDeadHosts(data):
    click.echo("\tHOST\t\t\t\tStatus")
    click.echo("================================================================================================================")
    for line in data:
        if 'Status: Down' in line:
            click.echo("\t"+line.split("Host: ")[1].split(" (")[0]+'\t------------\t'+line.split("Status: ")[1])


def printBanner(options):
    if all(o in options for o in ["h", "p", "s"]):
        click.echo("\tHOST\t\t\t\tPORT\t\t\t\tSERVICE")
        click.echo("================================================================================================================")
    elif all(o in options for o in ["h","p"]):
        click.echo("\tHOST\t\t\t\tPORT")
        click.echo("================================================================================================================")
    elif all(o in options for o in ["h", "s"]):
        click.echo("\tHOST\t\t\t\tSERVICE")
        click.echo("================================================================================================================")
    elif all(o in options for o in ["p","s"]):
        click.echo("\tPORT\t\t\t\tSERVICE")
        click.echo("================================================================================================================")
    elif all(o in options for o in ["h"]):
        click.echo("\tHOST")
        click.echo("================================================================================================================")
    elif all(o in options for o in ["s"]):
        click.echo("\tSERVICE")
        click.echo("================================================================================================================")
    elif all(o in options for o in ["p"]):
        click.echo("\tPORT")
        click.echo("================================================================================================================")


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [ atoi(c) for c in re.split(':', text) ]


def port_keys(text):
    return [ atoi(c) for c in text[1] ]


def convert_csv(input_data, input_file_name):
    rows = list()
    output_file =input_file_name.split('.')[0] + '.csv'

    for line in input_data:
        if '#' not in line:
            m = re.search('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s([^\)]+)\)', line)
            host = m.group()

            # grab all open ports after Ports:
            m = re.search('\d+/.+\t', line)
            if m:  # if no open ports, re search will be NoneType
                services = m.group().strip().split('/,')

            else:
                services = None
            if services:
                row = list()
                row.append(host)
                for s in services:
                    service = row + list(filter(lambda x: x != '', s.strip().split('/')))
                    rows.append(service)

    if rows:
        with open(output_file, 'wb') as f:
            fieldnames = ['host', 'port_num', 'state', 'proto', 'service', 'description']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in rows:
                writer.writerow(dict(zip(fieldnames, r)))
                # print host, services

        exit('[+] Done.', output_file)
    else:
        exit('[-] Nothing to convert')


if __name__ == '__main__':
    main(sys.argv[1:])  # passing sys.argv[1:] to disable Click from parsing as unicode. (needed for Pycharm to debug)
