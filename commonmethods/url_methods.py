#coding:utf-8
import urllib.request
import urllib.parse
import json
import string
import random
import mimetypes


class UrlMethods():
    def __init__(self):
        self.cookie="JSESSIONID=f83d36d18ccb4f57928fca0830e9a8bf; lang=zh_CN"
    def url_get_method(self,url):
        cookie=self.cookie
        req=urllib.request.Request(url)
        req.add_header('Cookie',cookie)
        req_urlopen=urllib.request.urlopen(req)
        f=req_urlopen.read().decode('utf-8')
        #json.loads(f)是将JSON编码的字符串转为python中dict类型
        get_rs=json.loads(f)
        return get_rs
    def url_post_method(self,url,post_data):
        cookie=self.cookie
        #post_data要求是dict类型
        data=urllib.parse.urlencode(post_data)
        data=data.encode('utf-8')
        req = urllib.request.Request(url)
        req.add_header('Cookie', cookie)
        req_post = urllib.request.urlopen(req,data)
        f = req_post.read().decode('utf-8')
        post_rs = json.loads(f)
        return post_rs
    #post方法传递的数据可以是dict，也可以是str，都需要encode
    # def url_post_str_data_method(self,url,str_data):
    #     cookie=self.cookie
    #     req=urllib.request.Request(url,str_data.encode('utf-8','ignore'))
    #     req.add_header('Cookie',cookie)
    #     req_str_data=urllib.request.urlopen(req)
    #     f=req_post_str.read().decode('utf-8')
    #     str_rs=json.loads(f)
    #     return str_rs
    #上传图片
    def url_image_upload_method(self,url,image_data,headers):
        req=urllib.request.Request(url,image_data.encode('ISO-8859-1','ignore'))
        req.add_header('Content-Type' ,headers['Content-type'])
        req.add_header('Content-Length' ,headers['Content-Length'])
        req.add_header('Cookie','JSESSIONID = 2614a269ec7540cb810de32cc707b0ad;lang = zh_CN')
        try:
            req_image_upload=urllib.request.urlopen(req)
            f = req_image_upload.read().decode('utf-8')
            return f
        except urllib.error.HTTPError as e:
            print(e.code)
            print(e.read())


    #上传图片前生成multipart/form-data数据
    def url_multipart_formdata(self,files,fields,boundary=None):
        '''Encode dict of form fields and dict of files as multipart/form-data.
        Return tuple of (body_string, headers_dict). Each value in files is a dict
        with required keys 'filename' and 'content', and optional 'mimetype' (if
        not specified, tries to guess mime type or uses 'application/octet-stream').'''
        #大小写字母string.ascii_letters:The concatenation of the ascii_lowercase and ascii_uppercase constants described below. This value is not locale-dependent.
        #数字string.digits:The string '0123456789'.
        _BOUNDARY_CHARS=string.digits+string.ascii_letters
        #str.replace(old, new[, max])replace() 方法把字符串中的 old（旧字符串） 替换成 new(新字符串)，如果指定第三个参数max，则替换不超过 max 次
        def escape_quote(s):
            return s.replace('"','\\"')

        if boundary is None:
            #random.choice(seq) Return a random element from the non-empty sequence seq. If seq is empty, raises IndexError.
            boundary=''.join(random.choice(_BOUNDARY_CHARS) for i in range(16))
        lines=[]

        for name,value in files.items():
            filename=value['filename']
            if 'mimetype' in value:
                mimetype=value['mimetype']
            else:
                mimetype=mimetypes.guess_type(filename)[0] or 'application/octet-stream'
            lines.extend((
                '------------WebKitFormBoundary{0}'.format(boundary),
                'Content-Disposition: form-data; name="{0}"; filename="{1}"'.format(escape_quote(name),escape_quote(filename)),
                'Content-Type: {0}'.format(mimetype),
                '',
                value['content'].read().decode('ISO-8859-1'),
            ))

        for name,value in fields.items():
            lines.extend((
                '------------WebKitFormBoundary{0}'.format(boundary),
                'Content-Disposition: form-data; name ="{0}"'.format(escape_quote(name)),
                '',
                str(value),
            ))
        lines.extend((
            '------WebKitFormBoundary{0}--'.format(boundary),
            '',
        ))

        body='\r\n'.join(lines)

        headers={
            'Content-type':'multipart/form-data; boundary=----WebKitFormBoundary{0}'.format(boundary),
            'Content-Length':str(len(body)),
        }
        
        return(body,headers)


# if __name__=='__main__':
#     um=UrlMethods()
#     tuple=um.url_multipart_formdata({'file':{'filename':'热火.jpg','content':''}},{'resourceId':'101018','resourceType':'menuitem201040','params':'{"11":{"w":80,"h":80,"x":78,"y":25},"34":{"w":80,"h":107,"x":0,"y":0},"169":{"w":86,"h":48,"x":0,"y":0}}'},boundary=None)
#     print(tuple[0])
#     print(tuple[1])










