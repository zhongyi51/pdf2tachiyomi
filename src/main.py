import argparse
import io
import os
import pdf2image
import requests
import zipfile


POPPLER_URL='https://github.com/oschwartz10612/poppler-windows/releases/download/v24.02.0-0/Release-24.02.0-0.zip'
def download_and_unzip_poppler(url, extract_to='./poppler'):
    print('Downloading poppler-windows...')
    response = requests.get(url)
    
    if response.status_code == 200:
        zip_file_bytes = io.BytesIO(response.content)
        
        with zipfile.ZipFile(zip_file_bytes, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f'Poppler extracted to {extract_to}')
        poppler_folder = [d for d in os.listdir(extract_to) if os.path.isdir(os.path.join(extract_to, d)) and d.startswith('poppler')]
        if len(poppler_folder)==0:
            raise ValueError('Poppler download fail')
        return os.path.join(extract_to,poppler_folder[0],'Library','bin')
    else:
        raise ValueError(f'Failed to download Poppler. Status code: {response.status_code}')

def parse_args():
    parser = argparse.ArgumentParser(description="Turn multi-page pdf into tachiyomi(mihon)-compatible files.")
    parser.add_argument('-f', type=str,help='PDF file path')
    parser.add_argument('-i', type=int,help='Chapter Name', default=1)
    parser.add_argument('-t', type=str,help='Target directory', default='./output')
    parser.add_argument('-p',type=str,help='Url to download poppler-windows',default=POPPLER_URL)
    
    return parser.parse_args()

def write_pngs(in_dir,out_dir,path):
    if not os.path.exists(in_dir):
        raise ValueError(f'path not exists: {in_dir}')
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    
    images=pdf2image.convert_from_path(in_dir,poppler_path=path,fmt="jpeg")
    print(f'page size:{len(images)}')
    for i,image in enumerate(images):
        image_f=os.path.join(out_dir,f'image_{i+1}.jpeg')
        print(f'writing image: image_{i+1} to {image_f}')
        image.save(image_f,format='jpeg')
        

if __name__ == "__main__":
    args=parse_args()
    path=download_and_unzip_poppler(args.p)
    print("start converting...")
    out_dir=os.path.join(args.t,f'chapter_{args.i}')
    write_pngs(args.f,out_dir,path)
    print("convert ok")
