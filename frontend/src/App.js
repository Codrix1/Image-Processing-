import "./App.css";
import Buttons from "./Componunts/Buttons";
import ImageUpload from "./Componunts/Uploader";
import Matching_upload from "./Componunts/matching_upload";
import ParticlesComponent from "./Componunts/particles";

const App = () => {
  return (
    <div className="App">
      <h1 className="Center">Image Filters</h1>
      <ParticlesComponent id="particles" />
      <div className="bigger_container">

        <div>
        <Buttons />
        </div>

        <div  className="Uploaders">
          <ImageUpload />
          <Matching_upload />
        </div>
        
      </div>
    </div>
  );
}

export default App;
