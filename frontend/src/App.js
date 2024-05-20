import "./App.css";
import Buttons from "./Componunts/Buttons";
import ImageUpload from "./Componunts/Uploader";
import ParticlesComponent from "./Componunts/particles";

const App = () => {
  return (
    <div className="App">
      
      <ImageUpload />

      <ParticlesComponent id="particles" />
      
      <Buttons />
      
      
    </div>
  );
}

export default App;
