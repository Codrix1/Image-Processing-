import Modal from "./modal";
import React, { useState } from "react";

const  Buttons = () => {

  const [OpenModel , setOpenModel] = useState(false)
  const [filter , setfilter] = useState()

  const apply_Filter = (clicked_button) => {
    
    setfilter(clicked_button);
    setOpenModel(true);

  }



    return (
    <div>

     
      <Modal source = {filter}/>
      <div className="main">
        <div className="Spatial_Domain containers">

          <div className="sub_containters">
            <h3 className="Center">Smoothing</h3>
            <button onClick={() => apply_Filter("Median")} className="button" >Median</button>
            <button onClick={() => apply_Filter("Adaptive")} className="button" >Adaptive</button>
            <button onClick={() => apply_Filter("Averaging")} className="button" >Averaging</button>
            <button onClick={() => apply_Filter("Gaussian")} className="button" >Gaussian</button>
            
          </div>
          <div className="sub_containters">
              <h3 className="Center">Sharpening</h3>
            <button onClick={() => apply_Filter("Laplacian")} className="button" >Laplacian</button>
            <button onClick={() => apply_Filter("Unsharp_Masking_and_Highboost")} className="button" >Unsharp Masking and Highboost</button>
            <button onClick={() => apply_Filter("Roberts_Cross_Gradient")} className="button" >Roberts Cross-Gradient </button>
            <button onClick={() => apply_Filter("sobya")} className="button" >sobya</button>
            
          </div>
          <div className="sub_containters">
            <h3 className="Center">Noise</h3>
            <button onClick={() => apply_Filter("Impulse_noise")} className="button" >Impulse noise</button>
            <button onClick={() => apply_Filter("Gaussian_noise")} className="button" >Gaussian noise</button>
            <button onClick={() => apply_Filter("Uniform_noise")} className="button" >Uniform noise</button>
          
          </div>
        </div>
        
        <div className="Frequency_Domain containers2">
        <h2 className="Center" >Frequency Domain</h2>

          <button onClick={() => apply_Filter("Histogram_Equalization")} className="button" >Histogram Equalization</button>
          <button onClick={() => apply_Filter("Histogram_Specification")} className="button" >Histogram Specification</button>
          <button onClick={() => apply_Filter("Fourier_transform")} className="button"> Fourier transform </button>
          <button onClick={() => apply_Filter("Interpolation")} className="button" >Interpolation </button>

        </div>
        
      </div>

    </div>
    
  );
}
export default Buttons;