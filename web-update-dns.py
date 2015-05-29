#!/usr/bin/env python

# Import modules for CGI handling
import cgi
from IPy import parseAddress, IP
import re
from subprocess import Popen, PIPE

DNSCMD = 'c:\windows\system32\dnscmd.exe'
NSLOOKUPCMD = r'c:\windows\system32\nslookup.exe'
DOMAINCONTROLLER = 'dc1.presidiolab.local'
DNSZONE = 'presidiolab.local'
PASSWORD = 'Gt500gelf'

# Create instance of FieldStorage
form = cgi.FieldStorage()
# Get data from fields
ip_address = form.getvalue('ip_address')

if form.getvalue('fqdn') is None:
    fqdn = 'blank'
else:
    fqdn = form.getvalue('fqdn')

action = form.getvalue('action')
password = form.getvalue('password')


def is_valid_ip(ip_address):
    try:
        ip = parseAddress(ip_address)
    except Exception:
        return False
    if not ip:
        return False
    else:
        return ip[0]


def get_in_addr(ip_address):
        return IP(ip_address).reverseName()


def is_valid_fqdn(fqdn):
        try:
            if len(fqdn) > 255:
                    return False
        except:
            return False
        if fqdn[-1] == ".":
                fqdn = fqdn[:-1]
        allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
        return all(allowed.match(x) for x in fqdn.split("."))


def is_valid_action(action):
    if action == 'add' or action == 'delete':
        return True
    else:
        return False


def is_valid_password(password):
    if password == PASSWORD:
        return True
    else:
        return False


def is_form_valid(ip_address, fqdn, action, password):
    valid_fqdn = is_valid_fqdn(fqdn)
    valid_ip = is_valid_ip(ip_address)
    valid_action = is_valid_action(action)
    valid_password = is_valid_password(password)
    if valid_fqdn and valid_ip and valid_action and valid_password:
        return True
    else:
        return False


def get_existing_ptr_record(ip_address):
    proc_exist = Popen([NSLOOKUPCMD, ip_address, DOMAINCONTROLLER], stdout=PIPE)
    for i in proc_exist.stdout:
        reg_match = re.match("Name:\s+(\S+)", str(i), re.IGNORECASE)
        try:
            return reg_match.group(1)
        except:
            pass


def add_a_ptr_record(fqdn, ip_address):
    proc_a_ptr = Popen([DNSCMD, DOMAINCONTROLLER, '/RecordAdd', DNSZONE, fqdn.partition('.')[0].rstrip(), '/CreatePTR', 'A', ip_address], shell=True, stdout=PIPE)
    return proc_a_ptr.stdout


def delete_ptr_record(ip_address):
    in_addr = get_in_addr(ip_address)
    proc_ptr = Popen([DNSCMD, DOMAINCONTROLLER, '/RecordDelete', in_addr.split('.', 1)[1], in_addr.split('.', 1)[0], 'PTR', '/f'], shell=True, stdout=PIPE)
    return proc_ptr.stdout


def delete_a_record(fqdn, ip_address):
    proc_a = Popen([DNSCMD, DOMAINCONTROLLER, '/RecordDelete', DNSZONE, fqdn.partition('.')[0], 'A', ip_address, '/f'], shell=True, stdout=PIPE)
    return proc_a.stdout


def print_blank_html_form():
    print_html_header()


def print_html_header():
    print 'Content-type:text/html\r\n\r\n'
    print '<html>'
    print '<head>'
    print ' <title>DNS Updater</title>'
    print '</head>'


def print_html_form(valid_form, del_ptr_output, delete_a_output, add_a_ptr_output):
    print ' <body>'
    print '<samp>'
    print '<table align=left border=0 cellpadding=1 cellspacing=1 style=width:100%'
    print '   <table align=center border=0 cellpadding=1 cellspacing=1 style=width:100%>'
    print '     <tbody>'
    print '       <form action=./web-update-dns.py method=post>'
    print '       <tr>'
    print '         <td align="center">Hostname: <input placeholder=hostname type=text name=fqdn></td>'
    print '       </tr>'
    print '       <tr>'
    print '         <td align="center">IP Address: <input placeholder=10.0.0.1 type=text name=ip_address></td>'
    print '       </tr>'
    print '       <tr>'
    print '         <td align="center">Update Password: <input type=password name=password></td>'
    print '       </tr>'
    print '       <tr>'
    print '         <td align="center" width="500"><input type=radio name=action value=delete> Delete <input type=radio name=action value=add /> Update</td>'
    print '       </tr>'
    print '         <td align="center">'
    if valid_form:
        print 'DNS Record Updated Successfully!</td></tr>'
    else:
        print 'Please enter a valid IP address, hostname, action, and update password.</td></tr>'
    print '       <tr>'
    print '         <td align="center"><input type=submit value=Submit></td>'
    print '       </tr></table><br>'
    print '       <table align=left border=0 cellpadding=1 cellspacing=1 style=width:100%><tr><td align="center" width="1000">'
    try:
        for i in del_ptr_output:
            print i
    except:
        pass
    print '       </td></tr>'
    print '       <tr><td align="center" width="1000">'
    try:
        for i in delete_a_output:
            print i
    except:
        pass
    print '       </td></tr>'
    print '       <tr><td align="center" width="1000">'
    try:
        for i in add_a_ptr_output:
            print i
    except:
        pass
    print '       </td></tr>'
    print '       </form>'
    print '     </tbody>'
    print '   </table>'
    print '</table>'
    print '</samp>'


def print_html_footer():
    print ' </body>'
    print '</html>'

valid_form = is_form_valid(ip_address, fqdn, action, password)
del_ptr_output = []
delete_a_output = []
add_a_ptr_output = []

if valid_form:
    if action == 'add':
        cont = 1
        while cont == 1:
            existing_record = get_existing_ptr_record(ip_address)
            if existing_record:
                delete_a_output = delete_a_record(existing_record, ip_address)
                del_ptr_output = delete_ptr_record(ip_address)
                del existing_record
                #cont = 0
            else:
                if fqdn == 'blank':
                    pass
                    cont = 0
                else:
                    add_a_ptr_output = add_a_ptr_record(fqdn, ip_address)
                    cont = 0
    elif action == 'delete':
        cont = 1
        while cont == 1:
            existing_record = get_existing_ptr_record(ip_address)
            if existing_record:
                delete_a_output = delete_a_record(existing_record, ip_address)
                del_ptr_output = delete_ptr_record(ip_address)
                del existing_record
                #cont = 0
            else:
                cont = 0
                pass

    print_html_header()
    print_html_form(valid_form, del_ptr_output, delete_a_output, add_a_ptr_output)
    print_html_footer()

else:
    del_ptr_output = []
    delete_a_output = []
    add_a_ptr_output = []
    print_html_header()
    print_html_form(valid_form, del_ptr_output, delete_a_output, add_a_ptr_output)
    print_html_footer()
