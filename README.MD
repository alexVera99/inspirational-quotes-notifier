# Description
It sends notifications of inspirational quotes to your Mac to get you motivated and inspired. You can use setup a cronjob in order to automate the execution of the script. That way, you will get inspirational quotes during the day.
If you want to check how it works, please check this [post](https://www.devsfocus.com/post/inspirational-quotes-notifications-in-macos) in the blog [DevsFocus](https://www.devsfocus.com/)

Important! This only is supported for Mac. Mainly because of the notification library. In the future, it will support also Windows. However, if you want to do it, I will be more than happy to merge your code :)

# Set up
In order to facilitate its use, I have built a bash script called setup.sh. This will install python virtualenv in order to create a virtual environment where we are going to install everythin we need. Check the file requirements.txt if you want to know which python libraries we are using.
To use it, simply run

`bash setup.sh`

# Executing
You can run the `main.py` file as any other python file. I have create the bash script `run.sh` that activates the virtual environment and runs the `main.py` file. This makes easier the execution of the program if you want to use a cronjob.
To use it, simply run

`bash run.sh`

# Automate it to every our
The notifications are nice, but the cooler part is to automate the execution of the program. That way, you will have inspirational quotes every N time.
We can achieve this by using cronjob. You can refer to the [post](https://www.devsfocus.com/post/inspirational-quotes-notifications-in-macos) I mentioned before, or just follow this steps:
1. Open your terminal
2. Type: `crontab -e`
3. Press *i* key to be able to start typing
4. If you want to execute it every hour, type the following: 
`0 * * * * path_dir && bash run.sh`
  where *path_dir* is the directory where our script is located
5. Hit *ESC* key
6. Type "*:wq*" (without quotes)
7. A pop up may be shown from MacOS system asking to let the terminal modify your system. Simply accept it :)

And you are done, every hour the python app will be execute it and you will get a inspirational quote notifiation.

## Possible problems
To check if something have go wrong, got to var/mail. And open a file that probably has the name of your mac.
- It may happen that appears `bash: run.sh: Operation not permitted`. Try to move the project to another folder like Users/your_mac_name. This happens because in newer versions of MacOS, there are some folders where crontab does not have access. 
  
  If you prefer to place the project in this kind of places, you can refer to this [post](https://blog.bejarano.io/fixing-cron-jobs-in-mojave/) in order to do it. The solution is basically giving Full Disk Access to cron. However, I don't like this solution, that is why I recommend moving the projec to another folder.

# Known issues
- Sometimes it appears the error: 
```
Traceback (most recent call last):
  File "src/main.py", line 10, in <module>
    Notifier.notify(quote_text, title=quote_author + " once said:", group=os.getpid(), sound="Submarine")#, ignoreDnD=False)
TypeError: unsupported operand type(s) for +: 'NoneType' and 'str'
```
It's not solved yet, but probably the error is because the variable quote_author is empty for some reason.