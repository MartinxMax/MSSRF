  <div align="center">
 <p align="center">
 <img title="MSSRF" src='https://img.shields.io/badge/MSSRF-1.0.0-brightgreen.svg' />
 <img title="MSSRF" src='https://img.shields.io/badge/ThinkPHPV5.0.23-Tool'/>
 <img title="MSSRF" src='https://img.shields.io/badge/Python-3.9-yellow.svg' />
  <img title="MSSRF" src='https://img.shields.io/badge/HackerTool-x' />
 <img title="MSSRF" src='https://img.shields.io/static/v1?label=Author&message=@Martin&color=red'/>
 <img title="MSSRF" src='https://img.shields.io/badge/-Linux-F16061?logo=linux&logoColor=000'/>
 </p>
  <img height="137px" src="https://github-readme-stats.vercel.app/api?username=MartinXMax&hide_title=true&hide_border=true&show_icons=trueline_height=21&text_color=000&icon_color=000&bg_color=0,ea6161,ffc64d,fffc4d,52fa5a&theme=graywhite" />
  
   
 <table>
  <tr>
      <th>Function</th>
  </tr>
  <tr>
    <th>
        SSRF attack
    </th>
  </tr>
 </table>
</div>

## usage method
  * View help information

      ```#python3 MSSRF.py -h```

  ![图片名称](./PT/help0.png)  

# Send request



Find injection point

  ![图片名称](./PT/use1.png)  

__PS:You must mark the injection point with * and write the request message required to access other websites into the Request.conf file__

 ```#python3 MSSRF.py -url http://61.147.171.105:50765/use.php?url=*```

  ![图片名称](./PT/SSRF.png)  
  
_The server successfully requested another page_
 
  ![图片名称](./PT/SSRF2.png)  
  