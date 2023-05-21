from typing import Any
from bson.json_util import dumps
from bson import ObjectId

from flask import Flask, render_template, request, jsonify
application = app = Flask(__name__) 

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.jy74xj7.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

#해당 팀원의 페이지로 이동하는 랜더링
@app.route('/memberid/<name>') #각 멤버의 페이지 url을 /members/<멤버의 firstname>으로 구분해 이동
def member_html(name):
    return render_template(f'/members/{name}.html')

@app.route('/edits/<editname>')
def edits_html(editname):
    return render_template(f'/edits/{editname}.html')

#팀원의 정보를 입력받아 저장하고 요청 시 정보를 내려주는 라우트 GET, POST
@app.route('/members', methods=["GET", "POST"])
def add_search():
    if request.method == 'POST' :
        name_receive = request.form['name_give']
        mbti_receive = request.form['mbti_give']
        advantage_receive = request.form['advantage_give']
        style_receive = request.form['style_give']

        doc = {
            'name' : name_receive,
            'mbti' : mbti_receive,
            'advantage' : advantage_receive,
            'style' : style_receive
        }
        name_list = list(db.memberInfo.find({},{'_id':False}))
        for a in name_list :
            if a['name'] == name_receive :
                return jsonify({'result': '이미 등록된 팀원입니다!'})   #이미 있는 팀원 이름이면 등록x
    
        if name_receive in ['박성민', '강영규', '곽현규', '심재두'] :
            db.memberInfo.insert_one(doc)
            return jsonify({'result': '저장 완료!'}) 
        else : 
            return jsonify({'result': '잘못된 이름입니다.'})     #팀원 4명의 이름 외 입력시 잘못된 이름이라 나옴
    elif request.method == 'GET':
        all_memberInfo = list(db.memberInfo.find({},{}))

        return jsonify({'result': dumps(all_memberInfo)})

#멤버 한명의 정보를 특정해서 가져오고 수정하고 삭제하기
@app.route('/member/<oid>', methods=["GET", "PUT", "DELETE"]) #아이고 저 @이거 없어가지고 여태 계속 해맸네..
def member_Info(oid):
    if request.method == 'GET':
        list_name = ['박성민', '강영규', '곽현규', '심재두']
        if oid in list_name :
            find_Info = [db.memberInfo.find_one({'name': oid}, {'name':False})]
            return jsonify({'result': dumps(find_Info)})
        else :
            find_Info = [db.memberInfo.find_one({'_id':ObjectId(oid)}, {'_id':False})]
            
            return jsonify({'result': find_Info})
    
    elif request.method == 'PUT':
        name_receive = request.form['name_give']
        mbti_receive = request.form['mbti_give']
        advantage_receive = request.form['advantage_give']
        style_receive = request.form['style_give']
        doc = {
            'name' : name_receive,
            'mbti' : mbti_receive,
            'advantage' : advantage_receive,
            'style' : style_receive
        }
        edit_a = db.memberInfo.find_one({'_id': ObjectId(oid)}, {'_id': False})
        if doc == edit_a :
            return jsonify({'result': '수정할 정보 없음!'})
        else :
            db.memberInfo.update_one({'_id': ObjectId(oid)}, {'$set' : doc})
        
        return jsonify({'result': '수정 완료!'})
    
    elif request.method == 'DELETE' :
        db.memberInfo.delete_one({'_id':ObjectId(oid)})
        
        return jsonify({'result': '삭제 완료!'})


@app.route('/guest', methods=[ "POST"])
def pageMember_Info() :
    pageName_receive = request.form['pageName_give']
    guest_name_receive = request.form['guest_name_give']
    guest_comment_receive = request.form['guest_comment_give']

    doc = {
        'pageName' : pageName_receive,
        'name' : guest_name_receive,
        'comment' : guest_comment_receive
    }
    db.guest_Info.insert_one(doc)
    return jsonify({'result': '저장 완료!'})

    
@app.route('/guest_edit/<oid>', methods=["PUT", "DELETE"])
def guest_edits(oid) :
    if request.method == "DELETE":    
        print(oid) 
        db.guest_Info.delete_one({'_id':ObjectId(oid)})
        
        return jsonify({'result': '삭제 완료!'})

    elif request.method == 'PUT':
        name_receive = request.form['name_give']
        comment_receive = request.form['comment_give']

        doc = {
            'name' : name_receive,
            'comment' : comment_receive
        }
        edit_a = db.guest_Info.find_one({'_id': ObjectId(oid)}, {'_id': False, 'pageName': False})
        print(edit_a)
        if doc == edit_a :
            return jsonify({'result': '수정할 정보 없음!'})
        else :
            db.guest_Info.update_one({'_id': ObjectId(oid)}, {'$set' : doc})
        
        return jsonify({'result': '수정 완료!'})

@app.route('/guest/<oid>', methods=["GET"])
def guests_Info(oid) :
    find_guestInfo = list(db.guest_Info.find({'pageName': oid}, {}))
    return jsonify({'result': dumps(find_guestInfo)})
    
@app.route('/guests/<oid>', methods=["GET"])
def guest_Info(oid) :
    find_guestInfo = db.guest_Info.find_one({'_id': ObjectId(oid)}, {'_id': False})
    print(find_guestInfo)
    return jsonify({'result': find_guestInfo})

if __name__ == '__main__': 
    app.run(debug=True)