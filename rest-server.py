from flask import Flask, make_response as _make_response
from merger import mergeInc, mergeFull
from overpass import getAddresses
from punktyadresowe_import import iMPA
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

def make_response(ret, code):
    resp = _make_response(ret, code)
    resp.mimetype ='text/xml; charset=utf-8'
    return resp

@app.route("/osm/adresy/iMPA/<name>.osm", methods=["GET", ])
def differentialImport(name):
    imp = iMPA(name)
    terc = imp.getConf()['terc']

    executor = ThreadPoolExecutor(max_workers=4)

    addr = executor.submit(lambda: getAddresses(terc))
    data = executor.submit(imp.fetchTiles)
    
    ret = mergeInc(addr.result(), data.result())
    
    return make_response(ret, 200)

@app.route("/osm/adresy/iMPA_full/<name>.osm", methods=["GET", ])
def fullImport(name):
    imp = iMPA(name)
    terc = imp.getConf()['terc']

    addr = getAddresses(terc) 
    data= imp.fetchTiles()
    
    ret = mergeFull(addr, data)
    
    return make_response(ret, 200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
