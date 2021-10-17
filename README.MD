# Description
It sends notifications of inspirational quotes to your Mac to get you motivated and inspired. 

You can set up a cronjob to automate the execution of the app. That way, you will get inspirational quotes during your day.

If you want to check how it works, please check this [post](https://www.devsfocus.com/post/inspirational-quotes-notifications-in-macos) in the blog [DevsFocus](https://www.devsfocus.com/)

<p align="center">
  <img src="https://static.wixstatic.com/media/2c7963_941ce98061644edaad0cb6dd0a3acf3e~mv2.jpg/v1/fill/w_598,h_127,al_c,q_90/2c7963_941ce98061644edaad0cb6dd0a3acf3e~mv2.webp" alt="Notification example"/>
</p>

Also, I have to thank the developer of the API: https://type.fit/api/quotes. It has been key in this project.

**Important!** This only is supported for macOS. Mainly because of the notification library. In the future, it will support Windows too. However, if you want to do it, I will be more than happy to merge your code :)

# Set up
To facilitate its use, I have built a bash script called `setup.sh`. This will install python virtualenv to create a virtual environment where we will install everything we need. Check the file `requirements.txt` to know which python libraries we are using in the project.

Then, to prepare everything to execute the app, simply type in your terminal

`bash setup.sh`

# Executing
You can run the `main.py` file as any other python file. Also, you can use the bash script `run.sh`, which executes the `main.py` file using the virtual environment setup.

To use it, simply use

`bash run.sh`

The main reason for doing this is to ease the execution of the program if you want to use a cron.

# Automate its execution every hour
The coolest part of the project is automating the execution of the program. That way, you will have inspirational quotes notifications every N time.
We can achieve this by using cron. You can refer to the [post](https://www.devsfocus.com/post/inspirational-quotes-notifications-in-macos) I mentioned before, or just follow these steps:
1. Open your terminal
2. Type: `crontab -e`
3. Press the *i* key to be able to start typing
4. If you want to execute it every hour, type the following: 
`0 * * * * path_dir && bash run.sh`
  where *path_dir* is the directory where our script is located
5. Hit the *ESC* key
6. Type "*:wq*" (without quotes)
7. A pop-up may be shown from the macOS system asking permissions for the terminal to modify your system. Simply accept it :)

And you are done! You will get inspirational quote notifications every hour.

## Possible problems
To check if something has gone wrong, go to `var/mail`. And open a file that probably has the name of your Mac.
- It may appear `bash: run.sh: Operation not permitted`. Try to move the project to another folder like `Users/your_mac_name`. This happens because, in newer versions of macOS, there are some folders where cron does not have access. 
  
  If you prefer to locate the project in this kind of folder, you can refer to this [post](https://blog.bejarano.io/fixing-cron-jobs-in-mojave/). The solution is basically giving Full Disk Access to cron. However, I don't like this solution since it may not be secure. That is why I recommend moving the project to another folder.