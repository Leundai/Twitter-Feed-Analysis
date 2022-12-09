import React from "react";
import { Container } from "@mui/system";

import "./AboutPage.css";
import { Button, Typography } from "@mui/material";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import { useNavigate } from "react-router-dom";

function AboutPage() {
  const navigate = useNavigate();

  return (
    <div>
      <Button
        onClick={() => navigate("/")}
        startIcon={<ArrowBackIcon />}
        color="info"
        size="medium"
        className="homepage-button"
      >
        Go Back
      </Button>
      <Container className="about-container" maxWidth="md">
        <div className="about-section">
          <Typography variant="h4" color="#29B6F6" marginBottom=".5em">
            Why?
          </Typography>
          <Typography variant="body1" color="white">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi
            malesuada sit amet enim in feugiat. Curabitur libero sem, iaculis eu
            nisl quis, dictum accumsan nisi. Fusce finibus augue a sapien
            mollis, ornare tempus tortor volutpat. Nunc quis tortor efficitur,
            vehicula dolor eu, euismod enim. Quisque quis tincidunt ante. Morbi
            vitae efficitur magna. Suspendisse condimentum iaculis elit vitae
            dapibus. Aenean sodales a elit vitae fermentum.
            <br />
            <br />
            In ac felis at tortor condimentum varius. Nulla sed quam eget ante
            pretium finibus eget sit amet lorem. Ut ac eros eget dui euismod
            congue. Nullam augue enim, scelerisque nec tempus vitae, egestas
            fringilla dui. Nam iaculis leo elit, at iaculis lectus convallis
            ullamcorper. Duis laoreet rhoncus tincidunt. Phasellus ullamcorper
            eu metus non eleifend. Nam sed diam egestas, volutpat urna quis,
            accumsan odio. Vivamus in urna risus. Ut a est ac orci dignissim
            vestibulum quis vitae dolor.
          </Typography>
        </div>
        <div className="about-section">
          <Typography variant="h4" color="#29B6F6" marginBottom=".5em">
            Why?
          </Typography>
          <Typography variant="body1" color="white">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi
            malesuada sit amet enim in feugiat. Curabitur libero sem, iaculis eu
            nisl quis, dictum accumsan nisi. Fusce finibus augue a sapien
            mollis, ornare tempus tortor volutpat. Nunc quis tortor efficitur,
            vehicula dolor eu, euismod enim. Quisque quis tincidunt ante. Morbi
            vitae efficitur magna. Suspendisse condimentum iaculis elit vitae
            dapibus. Aenean sodales a elit vitae fermentum.
            <br />
            <br />
            In ac felis at tortor condimentum varius. Nulla sed quam eget ante
            pretium finibus eget sit amet lorem. Ut ac eros eget dui euismod
            congue. Nullam augue enim, scelerisque nec tempus vitae, egestas
            fringilla dui. Nam iaculis leo elit, at iaculis lectus convallis
            ullamcorper. Duis laoreet rhoncus tincidunt. Phasellus ullamcorper
            eu metus non eleifend. Nam sed diam egestas, volutpat urna quis,
            accumsan odio. Vivamus in urna risus. Ut a est ac orci dignissim
            vestibulum quis vitae dolor.
          </Typography>
        </div>
      </Container>
    </div>
  );
}

export default AboutPage;
