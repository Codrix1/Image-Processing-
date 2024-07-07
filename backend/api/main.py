from filters import * ;
from flask import Flask, request ,jsonify , send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from PIL import Image
import io
import cv2


app = Flask(__name__)
CORS(app)

app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['PATH'] = os.path.dirname(os.path.realpath(__file__))

@app.route("/", methods=['GET'])
def check():
    return(jsonify({'success': 'api connected successfully'}),200)




#--------------------------------------------------------------------------------------#
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


#--------------------------------------------------------------------------------------#

@app.route('/upload/<string:type>', methods=['POST'])
def upload_file(type):
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        try:
            image = Image.open(io.BytesIO(file.read()))
            image.verify()
            
            file.seek(0) 
            filename = f'{type}.jpg'
            file.save(os.path.join(app.config['PATH'], f'{type}.jpg'))
            return jsonify({'success': 'File uploaded successfully', 'filename': filename}), 200
        except (IOError, SyntaxError) as e:
            return jsonify({'error': 'File is not a valid image'}), 400
    else:
        return jsonify({'error': 'File type not allowed'}), 400

#--------------------------------------------------------------------------------------#
@app.route("/edit",methods=['POST'])
def save_edited_image():
    try:
        script_dir = os.path.dirname(os.path.realpath(__file__))
        input_image_path = os.path.join(script_dir, 'original.jpg')
        output_image_path = os.path.join(script_dir, 'manipulatedImage.jpg')
        image = cv2.imread(output_image_path, cv2.IMREAD_COLOR)
        cv2.imwrite(input_image_path, image)
        return jsonify({'success': 'File uploaded successfully'}), 200
    except():
        return jsonify({'error': 'File upload unsuccessfull'}), 200


#--------------------------------------------------------------------------------------#
@app.route("/get/<string:type>")
def getOriginal(type):
    return send_file(f'{type}.jpg', mimetype='image/jpg' , as_attachment=True ) 



#--------------------------------------------------------------------------------------#

@app.route("/filters/<string:filter>" , methods = ["POST"])
def handle_json(filter ) :
    data = request.json
    
    match filter:
        case "Median":
            Window_size = int(data.get('Window_Size'))
            if Window_size < 3  or Window_size > 12: Window_size = 3
            Median(Window_size)  
        
        case "Adaptive":
            Window_size = int(data.get('Window_Size'))
            if Window_size < 3  or Window_size > 12: Window_size = 3
            adaptive_median_filter(Window_size)      
        
        case "Averaging":
            Window_size = int(data.get('Window_Size'))
            if Window_size < 3  or Window_size > 12: Window_size = 3
            Averaging(Window_size)  
        
        case "Gaussian_noise":
            Mean = float(data.get('Mean'))
            Standerd_deviation = float(data.get('Standerd_deviation'))
            create_gaussian_noise(Mean, Standerd_deviation)
            
        case "Uniform_noise":
            Level = int(data.get('Level'))
            if Level < 1  or Level > 150: Level = 1
            add_uniform_noise(Level)
            
        case "Unsharp_Masking_and_Highboost":
            k = float(data.get('K_value'))
            if k < 1: k = 1
            unsharp_masking_and_highboost_filtering(k)
            
        case "Gaussian":
            Window_size = int(data.get('Window_Size'))
            Sigma = float(data.get('Sigma'))
            if Window_size < 3  or Window_size > 12: Window_size = 3
            if Sigma < 1 or Window_size > 2: Sigma = 1

            gaussian_filter(Window_size , Sigma)
            
        case "Interpolation":
            type = str(data.get('type'))
            Resize = int(data.get('Resize'))
            if Resize < 1  or Resize > 4: Resize = 2
            if type == "nearest_neighbor": interpolation_nearest_neighbor(Resize)
            if type == "bilinear" : interpolation_bilinear(Resize)
        
        case "Laplacian":
            mode = str(data.get('modet'))
            apply_laplacian_operator()
            if mode =="mask_image": add_images()
            
        case "sobya":
            mode = str(data.get('modet'))
            sobya()
            if mode =="mask_image": add_images()
           
        case "Roberts_Cross_Gradient":
            mode = str(data.get('modet'))
            apply_roberts_operator()
            if mode =="mask_image": add_images()
           
        case "Histogram_Equalization":
            histogram_equalization()
            
        case "Histogram_Specification":
            histogram_specification()
        
        case "Fourier_transform":
            fourier()    
        
        case "Impulse_noise":
            salt = float(data.get('salt'))
            pepper = float(data.get('pepper'))
            if salt < 0.01  or salt > 0.4: salt = 0.05
            if pepper < 0.01  or pepper > 0.4: pepper = 0.05
            apply_impulse_noise(salt , pepper)
        
            
            
        case _ :
            return jsonify({"messege":"filter not yet added"}),202 
        
    return send_file('manipulatedImage.jpg', mimetype='image/jpg' , as_attachment=True ) 
        
            
           

    

    
    
    
    
if __name__ == "__main__":
    app.run(debug = True)