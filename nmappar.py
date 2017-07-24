import click

@click.command()
@click.option('--options', default="hps", help='number of greetings')
@click.option('--function', default="null", help='number of greetings')
@click.argument('file', type=click.File('rb'))
def main(options, function, file):
    data = file.readlines()
    opts = list(options)
    if function == 'print':
        printFile(data)
    if function.lower() == 'livehosts':
        printBanner(opts)
        getLiveHosts(opts, data)
    if 'search-service' in function.lower():
        term = function.split("=")[1]
        print term
        printBanner(opts)
        searchServices(opts, term.lower(), data)

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
                    pair = (line.split("Host: ")[1].split(" ()")[0],l.split('/open/tcp//')[0],l.split('/open/tcp//')[1])
                    list1.append(pair)
    printFunction(list1, opts)
def searchServices(opts, searchTerm, data):
    list1 = []
    for line in data:
        if 'Host:'in line and 'Ports:' in line:

            for l in line.split("Ports: ")[1].split(", "):
                if '/open/' in l:
                    pair = (line.split("Host: ")[1].split(" ()")[0],l.split('/open/tcp//')[0],l.split('/open/tcp//')[1])
                    if searchTerm in l.split('/open/tcp//')[1]:
                        list1.append(pair)
    printFunction(list1, opts)


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


if __name__ == '__main__':
    main()