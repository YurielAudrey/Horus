import configparser
import os


def save_csv_url(urls:list,path:str,encod:str):
    with open(path,"w",encoding=encod) as f:
        fl = ""
        for url in urls:
            fl = f"{fl},{url}"

        f.write(fl)
        f.close()

def load_url(path:str,encod:str)->list:
    with open(path,"r",encoding=encod) as f:
        urls=f.readline().split(',')
        return urls

def save_file(name_file:str,path,response):
    os.makedirs(os.path.dirname(f"{path}\\Horus"), exist_ok=True)
    p = f"{path}\Horus_{name_file}"
    with open(p, "wb") as f:
        f.write(response.content)
        f.close()
    return True

def save_cfg(**kwargs):
    config = configparser.ConfigParser()
    threads = kwargs['threads']
    path = kwargs['path']
    email = kwargs['email']

    config['Geral']= {'threads': threads,
                      'path':path,
                      'email':email
                      }

    config['Formatos']= {'img':kwargs['img'],
                         'videos':kwargs['videos'],
                         'text':kwargs['text'],
                         'all':kwargs["all"]
                         }

    with open('config/config.ini','w') as configfile:
        config.write(configfile)
        configfile.close()

def load_cfg():
    config = configparser.ConfigParser()

    config.read('config/config.ini')
    try:
        threads = int(config['Geral']['threads'])
        path = config['Geral']['path']
        email = config['Geral']['email']

        img_bool= bool(config['Formatos']['img'])
        video_bool = bool(config['Formatos']['videos'])
        text_bool = bool(config['Formatos']['text'])

        cfg = {
            "threads": threads,
            "path": path,
            "email": email,
            "img": img_bool,
            "video": video_bool,
            "text": text_bool
        }

        return cfg ,True
    except:
        cfg = {}
        return cfg, False



