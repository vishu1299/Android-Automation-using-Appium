import sys
import csv
import hashlib
import os
import glob
import unittest
from time import sleep
from appium import webdriver
import subprocess
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
email = ''
password = ''


######################################


def convert(somefile):
    #assuming file format : lastname,firstname,phonenumber,mail
    with open(somefile, 'r') as source, open('contacts.txt', 'w') as cunt:
        reader = csv.reader(source)
        allvcf = open('ALL.vcf', 'w')
        i = 0
        for row in reader:

            #write in the "ALL.vcf" file
            allvcf.write('BEGIN:VCARD' + "\n")
            allvcf.write('VERSION:3.0' + "\n")
            allvcf.write('N:' + row[0] + ';' + row[1] + "\n")
            allvcf.write('FN:' + row[1] + ' ' + row[0] + "\n")
            allvcf.write('TEL;CELL:' + row[8] + "\n")
            allvcf.write('END:VCARD' + "\n")
            allvcf.write("\n")
            cunt.write(f'{row[1]} {row[0]},{row[8]}\n')
            i += 1  # counts

        
        print(str(i) + " vcf cards generated")


convert('50-contacts.csv')

'''
def numlist_to_vcf(numfilename):
    try:
        with open(str(numfilename), 'r') as num_file, open('ALL.vcf', 'w') as allvcf, open('contacts.txt', 'w') as numname:

            allvcf.write(
                'BEGIN:VCARD\nVERSION:2.1\nN:first_name\nTEL;CELL:phone1\nEND:VCARD\n\n')

            for line in num_file:

                mob_num = line[:-1]
                hash_name = hashlib.md5(bytes(int(mob_num))).hexdigest()

                numname.write(f'num {hash_name},{mob_num}\n')

                #write in the "ALL.vcf" file.
                allvcf.write('BEGIN:VCARD\n')
                allvcf.write('VERSION:2.1\n')
                allvcf.write('N:' + f'{hash_name};num\n')
                allvcf.write('TEL;CELL:' + f'{mob_num[:3]}-{mob_num[3:6]}-{mob_num[6:]}\n')
                allvcf.write('END:VCARD\n')
                allvcf.write("\n")

        print("vcf cards generated")
        return True

    except:
        return False

# creates a name,num as well as corresponding vcf file
numlist_to_vcf('nums.txt')
'''

######################################


class AndroidWebViewTests(unittest.TestCase):

    def setUp(self):
        # change android version and platform version and device name accordingly
        desired_caps = {
            "platformName": "Android",
            "deviceName": "Android Emulator",
            "appPackage": "com.snapchat.android",
            "appActivity": "com.snapchat.android.LandingPageActivity"
        }

        self.driver = webdriver.Remote(
            'http://localhost:4723/wd/hub', desired_caps)

    def test_webview(self):
        #self.driver.press_keycode(4)
        #self.driver.push_file(r"/storage/emulated/0/ALL2.vcf",
                              #r"C:\Users\Vyprath\Downloads\ALL.vcf")

        subprocess.call("adb push ALL.vcf /sdcard/ALL.vcf", shell=True)
        print("pushed")
        self.driver.terminate_app('com.android.contacts')
        sleep(2)
        self.driver.start_activity("com.android.contacts", "com.android.contacts.activities.PeopleActivity")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//android.widget.ImageButton[@content-desc="Open navigation drawer"]'))).click()
        sleep(4)
        self.driver.swipe(170, 312, 240, 329, 1)
        sleep(2)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.LinearLayout[8]/android.widget.RelativeLayout'))).click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.LinearLayout[1]/android.widget.TextView'))).click()
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.Button[1]'))).click()
        except:
            pass
        sleep(2)
        allow1 = self.driver.find_element_by_id('com.google.android.documentsui:id/icon_thumb')
        allow1.click()
    
        #####SNAPCHAT######
        self.driver.launch_app()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.TextView[1]'))).click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[1]/android.widget.ScrollView/android.widget.LinearLayout/android.widget.EditText'))).send_keys(email)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[1]/android.widget.ScrollView/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.EditText'))).send_keys(password)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.LinearLayout'))).click()
        self.driver.terminate_app('com.android.contacts')
        sleep(2)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.Button'))).click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.Button[1]'))).click()
        sleep(2)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.Button[1]'))).click()
        sleep(2)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.Button[1]'))).click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.widget.FrameLayout[4]/android.widget.FrameLayout/android.widget.ImageView'))).click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[1]/android.view.View/javaClass[1]'))).click()
        sleep(1)
    
        try:
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[5]/android.widget.LinearLayout/android.view.View'))).click()
    
        except:
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, '/ hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout'))).click()

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/ hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.Button[1]'))).click()
        #WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.Button[1]'))).click()
        
        sleep(5)

        f = open('username.txt', 'w+')
        filehandle = open('contacts.txt','r')

        for line in filehandle:
            # remove linebreak which is the last character of the string
            details = line.split(',')
            name = details[0]
            #print(name)
            
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.view.ViewGroup/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.EditText'))).send_keys(name)
            try:
                WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[2]/android.view.View/android.view.View'))).click()
                try:
                    user = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup/android.widget.TextView[2]'))).text
                    print('method works')
                except:
                    el = self.driver.find_element_by_xpath(
                        '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup/android.widget.TextView[2]')
                    user = el.text
                number = details[1]
                f.write(f"{number[:-1]}:{user}\n")
                # back button
                button = self.driver.find_element_by_id('com.snapchat.android:id/profile_header_close_button')
                button.click()
            except:
                pass
        f.close()
        filehandle.close()

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(AndroidWebViewTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
