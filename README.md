# statusbot

A python script to send automated status update emails that are generated straight from your ics todo list.


## What is this for?

If you use [Rainlendar](http://rainlendar.net/cms/index.php) or any similar task management software which saves your todo list to an ICS file, this tool once properly configured will generate a status report of pending, wip and completed in the last 'x' days tasks and send it to your manager and team with one click.

## How to use

To use this, you will need to at the minimum:

1. Update the files under the templates folder to your taste
2. Update the following parameters in sendmail.py:
  2.1 <pathtoyourcalender>
  2.2 <yourmailserver>
  2.3 <youremail@yourcompany.com> (sender)
  2.4 <yourname> in the subject string
  2.5 The list of recipients: ["<yourmanager@yourcompany.com>", "<yourteam@yourcompany.com>"] 

After you've done this, running sendmail.py should send out a status email.
