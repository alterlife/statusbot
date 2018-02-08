import sys, os, stat, string, time, datetime, re
from smtplib import SMTP
from email.MIMEText import MIMEText
from icalendar import Calendar, Event


cal = Calendar.from_string(open('<pathtoyourcalender>\\default.ics','rb').read())


# formatTodo: Function to format a to-do mail
def formatToDo(cal, format):
    # Load the email templates
    f = open('templates/mail_template.html', 'r')
    mail_template = f.read()
    f.close()
    f = open('templates/task_template.html', 'r')
    task_template = f.read()
    f.close()

    # Build the array of completed, wip and todo items from the calender
    completed_items = []
    wip_items = []
    todo_items = []
    
    for component in cal.walk('VTODO'):
        if not 'STATUS' in component:
            continue
        if component['STATUS'] == 'COMPLETED': 
            days = abs(component['COMPLETED'].dt.replace(tzinfo=None) - datetime.datetime.now().replace(tzinfo=None)).days
            if days < 7: # We're interested only in completed items from the last 7 days.
                completed_items.append(component)
        else:
            if component['STATUS'] == 'IN-PROCESS':
                wip_items.append(component)
            else:
                todo_items.append(component)
                

    # Build report of completed items
    sl = 0
    completed_mail = ''
    for component in completed_items:
        sl = sl + 1

        progress = ''
        if 'PERCENT-COMPLETE' in component:
            progress = str(component['PERCENT-COMPLETE']) + '% complete'

        description = ''
        if 'DESCRIPTION' in component:
            description = component['DESCRIPTION']
        mailstring = task_template % ( sl, component['SUMMARY'], component['STATUS'], component['PRIORITY'], progress, description)
        completed_mail = completed_mail + mailstring

    # Build report of wip items
    wip_mail = ''
    for component in wip_items:
        sl = sl + 1

        progress = ''
        if 'PERCENT-COMPLETE' in component:
            progress = str(component['PERCENT-COMPLETE']) + '% complete'

        description = ''
        if 'DESCRIPTION' in component:
            description = component['DESCRIPTION']
            
        
        mailstring = task_template % ( sl, component['SUMMARY'], component['STATUS'], component['PRIORITY'], progress, description)
        wip_mail = wip_mail + mailstring

    # Build report of todo items
    todo_mail = ''
    for component in todo_items:
        sl = sl + 1

        progress = ''
        if 'PERCENT-COMPLETE' in component:
            progress = str(component['PERCENT-COMPLETE']) + '% complete'

        description = ''
        if 'DESCRIPTION' in component:
            description = component['DESCRIPTION']
            
        mailstring = task_template % ( sl, component['SUMMARY'], component['STATUS'], component['PRIORITY'], progress, description)
        todo_mail = todo_mail + mailstring

    # Put the lists into the email template
    mail = mail_template % (completed_mail, wip_mail, todo_mail)
    return mail

        

# Function to send an email status update
def sendemail(destination):
    SMTPserver = '<yourmailserver>'
    sender =     '<youremail@yourcompany.com>'
    
    subject="Goals as on " + str(datetime.datetime.now().date()) + " (<Your Name>)" # Update this
    content= formatToDo(cal, 'text')
    
    try:
        msg = MIMEText(content, 'html')
        msg['Subject']= subject
    
    
        conn = SMTP(SMTPserver)
        conn.set_debuglevel(True)
        try:
            conn.sendmail(sender, destination, msg.as_string())
        finally:
            conn.close()
    
    except Exception, exc:
        sys.exit( "mail failed: %s" % str(exc) )




sendemail(["<yourmanager@yourcompany.com>", "<yourteam@yourcompany.com>"]) 
