# hackernews-api-test
Testing the Hacker News public API

## Prerequisites:
Since I'm using Mac, I am listing the required software and tools needed prior to cloninng and running this project on your local machine.
1. Install Xcode
   2. Tip: first check if you already have Xcode installed. Type the following command in your Terminal: `$ /usr/bin/xcodebuild -version`
      3. If the response is Xcode and Build version numbers, then move to step 2; otherwise please proceed with the installation.
   4. Download Xcode from: https://developer.apple.com/xcode/ and then follow the installation instructions.
2. Install Homebrew
   3. Tip: first check if you already have Brew installed. Go to https://brew.sh/ and copy & paste the command listed in your Terminal.
   4. Next make sure to insert the HomeBrew directory on top of your PATH environment variable:
      5. Run the following in your Terminal: `$ touch ~/.bash_profile; open ~/.bash_profile`
      6. Add the following line at the bottom of your `~/.profile` file  `export PATH="/usr/local/opt/python/libexec/bin:$PATH"`
      7. If you have OS X 10.12 (Sierra) or older use this line instead `export PATH=/usr/local/bin:/usr/local/sbin:$PATH`
   8. Save and close the `~/.profile` file
3. Install Python3 with Brew
   4. First check the version you currently have by running: `$ python -V`
   5. If it's a version lower than python3, then you'll need to install the latest version using `brew`:
      6. Run the following in your Terminal: `$ brew install python`
7. Virtual Environment
   8. Install python3-pip by running these 2 commands in your Terminal:
      9. `$ python3 -m pip install --upgrade pip`
      10. `$ python3 -m pip --version`
   11. To create a new virtual environment run: `$ python3 -m venv .venv` inside your project directory
   12. To activate your newly created virtual environment run: `$ source .venv/bin/activate`
       13. To confirm the virtual environment is activated, check the location of your Python interpreter:
           14. `$ which python`
           15. While the virtual environment is active, the above command will output a filepath that includes the .venv directory, by ending with the following: `.venv/bin/python`.

Install packages
- Activate your virtual environment and install the `Requests` library:
  - `$ python3 -m pip install requests`

