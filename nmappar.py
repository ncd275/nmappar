import click
import re


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
        term = function.split("=")[1]
        printBanner(opts)
        searchServices(opts, term.lower(), data)
    if 'uniq-service' in function.lower():
        printBanner(["p","s"])
        uniqServices(opts, data)
    if 'search-port' in function.lower():
        portStr = function.split("=")[1]
        ports = []
        if ',' in portStr:
            ports = portStr.split(",")
        else:
            ports.append(portStr)

        printBanner(opts)
        searchPorts(opts, ports, data)

def printFile(data):
    click.echo(data)

def printFunction(portsNservices, options):

        if all(o in options for o in ["h","p","s"]):
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
                        pair = (line.split("Host: ")[1].split(" ()")[0],re.split("/open/[^\s]*?//", l)[0],re.split("/open/[^\s]*?//", l)[1].split("\tIgnored State:")[0]+"\n")
                    else:
                        pair = (line.split("Host: ")[1].split(" ()")[0],re.split("/open/[^\s]*?//", l)[0],re.split("/open/[^\s]*?//", l)[1])
                    list1.append(pair)
    printFunction(list1, opts)
def searchServices(opts, searchTerm, data):
    list1 = []
    for line in data:
        if 'Host:'in line and 'Ports:' in line:

            for l in line.split("Ports: ")[1].split(", "):
                if '/open/' in l:
                    if 'Ignored State' in l:
                        pair = (line.split("Host: ")[1].split(" ()")[0],re.split("/open/[^\s]*?//", l)[0],re.split("/open/[^\s]*?//", l)[1].split("\tIgnored State:")[0])
                    else:
                        pair = (line.split("Host: ")[1].split(" ()")[0],re.split("/open/[^\s]*?//", l)[0],re.split("/open/[^\s]*?//", l)[1])
                    if searchTerm.lower() in pair[2].lower():
                        list1.append(pair)
    try:
        list1.sort(key=lambda x: int(x[1]))
    except:
        pass
    printFunction(list1, opts)

def searchPorts(opts, ports, data):
    list1 = []
    pair = ''
    for line in data:
        if 'Host:'in line and 'Ports:' in line:

            for l in line.split("Ports: ")[1].split(", "):
                if '/open/' in l:
                    if 'Ignored State' in l:
                        pair = (line.split("Host: ")[1].split(" ()")[0],re.split("/open/[^\s]*?//", l)[0],re.split("/open/[^\s]*?//", l)[1].split("\tIgnored State:")[0])
                    else:
                        pair = (line.split("Host: ")[1].split(" ()")[0],re.split("/open/[^\s]*?//", l)[0],re.split("/open/[^\s]*?//", l)[1])

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
                        all_services.append("\t"+re.sub(r"/open/[^\s]*?//", ": --------------- \t",port).replace("\n","").split("\tIgnored State:")[0])
                    else:
                        all_services.append("\t"+re.sub(r"/open/[^\s]*?//", ": --------------- \t",port).replace("\n",""))


    uniq = set(all_services)
    for service in uniq:
        uniq_services.append(service)
    try:
        uniq_services.sort(key=lambda x: int(x.split(":")[0]))
    except:
        pass
    for service in uniq_services:
        click.echo(service)


def getDeadHosts(data):
    click.echo("\tHOST\t\t\t\tStatus")
    click.echo("================================================================================================================")
    for line in data:
        if 'Status: Down' in line:
            click.echo("\t"+line.split("Host: ")[1].split(" ()")[0]+'\t------------\t'+line.split("Status: ")[1])


def printBanner(options):
    if all(o in options for o in ["h","p","s"]):
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


if __name__ == '__main__':
    main()