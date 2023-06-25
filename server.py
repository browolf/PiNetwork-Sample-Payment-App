from flask import Flask, render_template
import random
import requests

app = Flask(__name__)


def payment(payment_id,action,txid=""):
    header = {
        #note value starts with "Key "
        'Authorization' : "Key yourapikey"
    }
    approveurl = f"https://api.minepi.com/v2/payments/{payment_id}/{action}"
    data = {'txid': txid} if txid else {}
    response = requests.post(approveurl,headers=header,data=data)
    if response.status_code == 200:
        res=f"Payment {action} request sent successfully"
    else:
        res = f"Failed to send payment {action} request. Status code: {response.status_code}"
        print (response.content)
    return res


@app.route("/")
def hello():
    payment_code = round(random.random(),7)      
    return render_template('main.html', amount=payment_code)


@app.route('/payment/<action>/<payment_id>', methods=['Get'])
def action_payment(action,payment_id):
    res=payment(payment_id,action)
    return res   


@app.route('/complete/<payment_id>/<txid>', methods=['Get'])
def complete_payment(payment_id,txid):
    res=payment(payment_id,"complete",txid)
    return res  

if __name__ == "__main__":
   app.run(host='0.0.0.0')
