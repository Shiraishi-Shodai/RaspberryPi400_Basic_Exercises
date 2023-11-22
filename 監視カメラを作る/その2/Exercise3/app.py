from flask import render_template, Flask, Response, request
import cv2

app = Flask(__name__, template_folder="./templates", static_folder="./static")

cap = cv2.VideoCapture(0, cv2.CAP_MSMF)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
cap.set(cv2.CAP_PROP_FPS, 1)           # カメラFPSを60FPSに設定(1秒間に60枚表示)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 300) # カメラ画像の横幅を1280に設定
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 200) # カメラ画像の縦幅を720に設定

def gen_frames():
    
   while True:
       ret, frame = cap.read()
       if not ret:
           break
       else:           
           #フレームデータをjpgに圧縮(ret: bool, buffer: ndarray)
           ret, buffer = cv2.imencode('.jpg',frame)
           # bytesデータ化
           frame = buffer.tobytes()

            # yield 莫大な量の戻り値を小分けにして返すことが出来る
            # 新しいフレーム（画像）をブラウザに送信
       yield (b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
   cap.release()

@app.route('/video_feed')
def video_feed():
    # HTTPレスポンス
   #imgタグに埋め込まれるResponseオブジェクトを返す
    # デフォルトでは、ResponseオブジェクトはHTMLのmimetypeを持ちます。つまり、デフォルトのContent-Typeヘッダーは"text/html"に設定されています。
    # mimetype='multipart/x-mixed-replace; boundary=frame'は、HTTPレスポンスのContent-Typeヘッダーを設定します。
    # このヘッダーは、レスポンスの形式をブラウザに伝えます。multipart/x-mixed-replaceは、マルチパートレスポンスの各部分が前の部分を置き換えることを示します。これにより、ブラウザは新しい画像フレームを受信するたびに、前のフレームを新しいフレームで置き換え、リアルタイムのビデオストリームを表示します。

    # boundary: HTTPレスポンスの情報を1つずつ区別するために用いる
    '''
    例)
    
    Content-Type: multipart/form-data; boundary=aBoundaryString
    (マルチパート文書全体に関連付けられる、他のヘッダー)

    (データ)
    --aBoundaryString
    Content-Disposition: form-data; name="myField"

    (データ)
    --aBoundaryString
    (サブパート)
    --aBoundaryString--
    '''

    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture')
def capture():
    ret, frame = cap.read()
    capture_error = ""

    if not ret:
        capture_error="キャプチャーエラー"
    else:
        cv2.imwrite("./static/img/picture.jpg", frame)

    return render_template('capture.html', capture_error=capture_error)

@app.route('/save', methods=["POST"])
def save():
    if request.method == "POST":
        img = cv2.imread("./static/img/picture.jpg")    
        file_name = request.form["file_name"] + ".jpg"
        cv2.imwrite(file_name, img)
        # cap.release()

        return  "保存しました"
@app.route('/')
@app.route('/index')
def index():
   
   return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)