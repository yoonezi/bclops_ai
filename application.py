from flask import Flask, request, jsonify
import sys
sys.path.insert(0, './src')

import os
import sys
import importlib.util


app = Flask(__name__)

@app.route('/ai', methods=['GET'])
def handle_request():
    
    main_dir = os.path.dirname(os.path.abspath(__file__))
    main_py_dir = os.path.join(main_dir, 'src')
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(current_dir, 'src')

    # url_param.txt 파일 경로
    url_param_path = os.path.join(main_py_dir, 'url_param.txt')
    url_param = request.args.get('url')
    
    if url_param:
        print(f"Extracted URL: {url_param}")
        with open(url_param_path , 'w') as file:
            file.write(url_param)
            
        # 다음 작업 수행
        os.chdir(src_dir)
        sys.path.append(src_dir)

        src_main_path = os.path.join(src_dir, 'main.py')
        spec = importlib.util.spec_from_file_location("main", src_main_path)
        main = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(main)
        
        # main.main()
        
        return f"Received URL: {url_param}"
    else:
        return "URL parameter not found"

    # if url_param:
    #     print(f"Extracted URL: {url_param}")
    #     with open(url_param_path , 'w') as file:
    #         file.write(url_param)
            
    #     return f"Received URL: {url_param}"
    # else:
    #     return "URL parameter not found"
    
  
    # os.chdir(src_dir)

    # sys.path.append(src_dir)

    # src_main_path = os.path.join(src_dir, 'main.py')
    # spec = importlib.util.spec_from_file_location("main", src_main_path)
    # main = importlib.util.module_from_spec(spec)
    # spec.loader.exec_module(main)
    
    # # main.main()


if __name__ == '__main__':
    # AWS Elastic Beanstalk에서 제공하는 환경 변수 'PORT'를 사용
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
