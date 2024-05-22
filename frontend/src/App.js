import "./App.css";
import Buttons from "./Componunts/Buttons";
import ImageUpload from "./Componunts/Uploader";
import Matching_upload from "./Componunts/matching_upload";
import ParticlesComponent from "./Componunts/particles";

const App = () => {
  return (
    <div className="App">
      <h1 className="Center">Image Filters</h1>
      <ImageUpload className="absolute top-50% left-50%" />

      <ParticlesComponent id="particles" />
      
      <Buttons />

      <Matching_upload />

    </div>
  );
}

export default App;
