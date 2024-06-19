1, Cài đặt python > 3.8
    1.1) apk add --no-cache python3 py3-pip
    1.2) apk --update --upgrade add gcc musl-dev jpeg-dev zlib-dev libffi-dev cairo-dev pango-dev gdk-pixbuf-dev python3-dev
    1.3) /usr/bin/python3.8 -m pip install --upgrade pip
2) Cài đặt packages
    2.1) pip3 install -r requirements.txt 

3) build file binary
    3.1) pyinstaller  --onefile build.spec
    3.2) cp dist/ovsftp ../ovsftp_bin
    
4) Kiểm tra
    4.1) ./ovsftp_bin -r "/ETON/QAS/SAP/Processed/Outbound/RET_TEST" -l "/app/RET_TEST" -t 30 -d true