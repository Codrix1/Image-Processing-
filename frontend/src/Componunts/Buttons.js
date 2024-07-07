import Modal from "./modal";
import React, { useState } from "react";

const Buttons = () => {
  const [OpenModel, setOpenModel] = useState(false);
  const [filter, setFilter] = useState();

  const applyFilter = (clickedButton) => {
    setFilter(null); // Temporarily set filter to null to ensure state change is detected
    setTimeout(() => {
      setFilter(clickedButton);
      setOpenModel(true);
    }, 50);
  };

  return (
    <div>
      <Modal source={filter} />
      <div className="main_container">
        <div className="big_container">
          <div className="Spatial_Domain containers">
            <div className="sub_containters">
              <h3 className="Center">Noise</h3>
              <button
                onClick={() => applyFilter("Impulse_noise")}
                className="button"
              >
                Impulse noise
              </button>
              <button
                onClick={() => applyFilter("Gaussian_noise")}
                className="button"
              >
                Gaussian noise
              </button>
              <button
                onClick={() => applyFilter("Uniform_noise")}
                className="button"
              >
                Uniform noise
              </button>
            </div>

            <div className="sub_containters">
              <h3 className="Center">Smoothing</h3>
              <button onClick={() => applyFilter("Median")} className="button">
                Median
              </button>
              <button onClick={() => applyFilter("Adaptive")} className="button">
                Adaptive
              </button>
              <button
                onClick={() => applyFilter("Averaging")}
                className="button"
              >
                Averaging
              </button>
              <button onClick={() => applyFilter("Gaussian")} className="button">
                Gaussian
              </button>
            </div>
            <div className="sub_containters">
              <h3 className="Center">Sharpening</h3>
              <button
                onClick={() => applyFilter("Laplacian")}
                className="button"
              >
                Laplacian
              </button>
              <button
                onClick={() => applyFilter("Unsharp_Masking_and_Highboost")}
                className="button"
              >
                Unsharp Masking and Highboost
              </button>
              <button
                onClick={() => applyFilter("Roberts_Cross_Gradient")}
                className="button"
              >
                Roberts Cross-Gradient
              </button>
              <button onClick={() => applyFilter("sobya")} className="button">
                sobya
              </button>
            </div>
          </div>

          <div className="Frequency_Domain containers">
            <h2 className="Center">Frequency Domain</h2>

            <button
              onClick={() => applyFilter("Histogram_Equalization")}
              className="button"
            >
              Histogram Equalization
            </button>
            <button
              onClick={() => applyFilter("Histogram_Specification")}
              className="button"
            >
              Histogram Specification
            </button>
            <button
              onClick={() => applyFilter("Fourier_transform")}
              className="button"
            >
              Fourier transform
            </button>
            <button onClick={() => applyFilter("Interpolation")} className="button">
              Interpolation
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
export default Buttons;
