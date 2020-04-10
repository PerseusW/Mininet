# Assignment 0: Getting start
## Due Sep 11, 2019, 11:59PM (GMT+8)
### Part 0 Build your coding environment
You SHOULD already have a coding environment involving `gcc/g++` `python` `git` `python3` and be able to link `dynamic lib`. If not, we recommend you using [Ubuntu](https://ubuntu.com/download/desktop) in [virtue](https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=ubuntu&rsv_pq=8398d0d200a39636&rsv_t=7d3cwHv0lro9uwWvbfXx05J5VhHynVdwMBqvLWjewSaFtmSJFhvXSQ%2F4K74&rqlang=cn&rsv_enter=1&rsv_dl=tb&rsv_sug3=7&rsv_sug1=5&rsv_sug7=101&rsv_sug2=0&inputT=1004&rsv_sug4=1629&rsv_sug=2) or [entity](https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=ISO%E5%AE%89%E8%A3%85ubuntu&oq=vmware%2520workstation%2520%25E5%25AE%2589%25E8%25A3%2585ubuntu&rsv_pq=a9978c1f00b4bc28&rsv_t=62c7FNYTcktZpV%2FLAJdq8f4uYdsJEQOBznWIV05%2BnZyEdx0vJExlpQRG39I&rqlang=cn&rsv_enter=1&rsv_dl=tb&inputT=32405&rsv_sug3=64&rsv_sug1=44&rsv_sug7=100&rsv_sug2=0&rsv_sug4=34298).

In the following part of this and many next README files, the notation:
+ `$: command line in Ubuntu/Debian Terminal`
+ `#: some commends/description`
+ `mininet> commands in Mininet`
+ `'something_more' ''`

After you set up your Ubuntu system,

`
$ sudo apt-get install cmake g++ git python3-dev qt5-qmake qt5-default python python3
`

I personally recommend [anaconda](https://www.anaconda.com/distribution/#download-section) as the python developing toolkit with [Jupyter Notebook](https://jupyter.org/install).
In the future work we will provide a `.ipynb` file helping you run a real-time feedback python script. So please install anaconda and Jupyter-Notebook in your Ubuntu system.
````
(Warning) the following steps may not work on some computers
TRY to solve them and feel free to contact TAs(TAs: No, we are not free, DO it YOURSELF).

$ cd ~/Desktop
$ mkdir temp
$ cd temp

$ wget https://repo.anaconda.com/archive/Anaconda3-2019.07-Linux-x86_64.sh

# Instead of wget you may also download this file manually
# https://www.anaconda.com/distribution/#download-section
# then choose Python3.7 version Linux 64bit x86 installer

$ sudo chmod u+x Anaconda3-2019.07-Linux-x86_64.sh
$ sudo ./Anaconda3-2019.07-Linux-x86_64.sh
# Then follow the Installation step

# reboot your system | $ sudo reboot

# After reboot type $ conda , then maybe the Terminal will return an error command
# This is caused with missing link Conda to Terminal -> you can add PATH to .bashrc or source
# Please google/baidu it and try to solve them
# After that don't forget $ conda init bash  #for Ubuntu only
# You should see (base) ...$  

(Optional) you should set a individual workspace for your python/conda environment
Something like $ conda create -n your_env_name python=3.7
If you wanna use this envs -> activate it $ conda activate your_env_name
if you need to see all your environments $ conda info --envs (多个环境独立使用可以起到隔离保护的作用)

# In (Base) or (your_env_name) to install Jupyter notebook
$ conda install jupyter jupyter notebook python
$ jupyter notebook

If you meet the IMPORT error you can install missing lib via $ conda install 'missing_lib'
Or $ pip install 'missing_lib'
(Clearly the best way is to Google the solution)
````
### Part 1 Git and GitHub
How to use git && GitHub:

Register a GitHub account if you haven't, then:
````
$ git config --global user.name "YOUR-SCREEN-NAME"
$ git config --global user.email YOUR-EMAIL-ADDRESS
````
Feel free to get more [infomation](https://git-scm.com/book/zh/v2)

You will receive your homework assignments, accept it then you will get a git repo whose link as `YOUR_HW_LINK`(i.e. https://github.com/NJU-CS-network-19-fall/assignment-number-your_screen_name)

**Please ALERT the DDL, GitHub will close automatically**
````
$ cd ~/Desktop/
$ mkdir hw
$ cd hw`
$ git clone YOUR_HW_LINK
# maybe need your GitHub account and passwords

# Code with FUN!!!
# ONLY KEEP CHANGE IN YOUR ASSIGNMENT-NUMBER FOLDER
# BECAUSE GIT ONLY SUBMIT WHAT'S IN THE FOLDER (.git)

# Once you finished
# In the ASSIGNMENT-NUMBER folder
$ git add -A
$ git commit -m "some words/marks"
$ git push origin master
# maybe need your GitHub account and passwords
````

例如当你git clone Assignment-0-your_screen_name后在文件夹中有这个README以及一个文件(还有一个.git/含有git branch的控制信息)


### Part 2 Who are you
注意 请将该目录下的文件改名为 你的中文姓名-你的学号 （注意中间有个-） 、
完成后,在Assignment-0-your_screen_name这个文件夹下：
````
$ git add -A
$ git commit -m "你的姓名(中英文随意)"
$ git push origin master
````


### Part 3 Mininet

In the first experiment we will use a simulation tool named [Mininet](http://mininet.org/).
Try to [install](http://mininet.org/download/) it on your Ubuntu system.

We recommend you install Mininet via Option 2 or 3, but Option 1 always works.

In Option 2, you can also run these commands to get latest mininet:
````
$ git clone git://github.com/mininet/mininet
$ cd mininet
$ git fetch
$ git checkout master
$ git pull
$ sudo make install
$ sudo util/install.sh -a
````

If you choose Option 1, after you open the VM(username and password are both 'mininet'), you can also install a working GUI consider now is already in 9012：

````
These commands are typed in the VM
Update:$ sudo apt-get update
Install the lxde desktop environment:$ sudo apt-get install xinit lxde
Install VirtualBox guest additions:$ sudo apt-get install virtualbox-guest-dkms
Restart the VM:$ sudo reboot
Start the GUI using: $ startx
````

After finishing installation, check the [tutorial](http://mininet.org/walkthrough/), you will need it in Assignment-1. \
To check if your installation is correct and complete  \
`$ sudo mn --version # should be 2.3.0, if not the newest version, update it via Option 4`.
