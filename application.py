from flask import Flask, request
import os
import sys
import importlib.util

app = Flask(__name__)

@app.route('/ai', methods=['GET'])
def handle_request():
    main_dir = os.path.dirname(os.path.abspath(__file__))
    main_py_dir = os.path.join(main_dir, 'src')
    src_dir = os.path.join(main_dir, 'src')

    url_param_path = os.path.join(main_py_dir, 'url_param.txt')
    distance_param_path = os.path.join(main_py_dir, 'distance_param.txt')
    
    url_param = request.args.get('url')
    distance_param = request.args.get('distance') 
    
    if url_param:
        with open(url_param_path, 'w') as file:
            file.write(url_param)
        with open(distance_param_path, 'w') as file:
            file.write(distance_param)

        os.chdir(src_dir)
        sys.path.append(src_dir)

        src_main_path = os.path.join(src_dir, 'main.py')
        spec = importlib.util.spec_from_file_location("main", src_main_path)
        main = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(main)

        return f"Received URL: {url_param} and Distance: {distance_param}"
    else:
        return "URL parameter not found"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)
