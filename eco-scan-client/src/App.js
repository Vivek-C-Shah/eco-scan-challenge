import React, { useState } from "react";
import UploadImage from "./components/UploadImage";
import Results from "./components/Results";
import Offers from "./components/Offers";
import {
  Container,
  AppBar,
  Toolbar,
  Typography,
  Card,
  CardContent,
  Button,
} from "@mui/material";

function App() {
  const [results, setResults] = useState(null);
  const [ecoScore, setEcoScore] = useState(null);
  const [showOffers, setShowOffers] = useState(false);

  return (
    <div
      style={{
        backgroundImage: `url(${process.env.PUBLIC_URL}/bg.png)`,
        backgroundSize: "cover",
        backgroundPosition: "center",
        minHeight: "100vh",
        padding: "1rem 0",
      }}
    >
      <AppBar position="static" sx={{ backgroundColor: "rgb(82, 110, 72)" }}>
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Welcome to EcoScan
          </Typography>
        </Toolbar>
      </AppBar>

      <Container
        maxWidth="md"
        style={{
          marginTop: "2rem",
          backgroundColor: "rgb(161, 238, 189)",
          borderRadius: "16px",
        }}
      >
        <Card variant="outlined" style={{ marginBottom: "2rem" }}>
          <CardContent>
            <UploadImage setResults={setResults} />
          </CardContent>
        </Card>

        {results && (
          <Card variant="outlined" style={{ marginBottom: "2rem" }}>
            <CardContent>
              <Results data={results} setEcoScore={setEcoScore} />
              {ecoScore && (
                <Button
                  variant="contained"
                  color="primary"
                  onClick={() => setShowOffers(!showOffers)}
                >
                  {showOffers ? "Hide Offers" : "List Offers"}
                </Button>
              )}
            </CardContent>
          </Card>
        )}

        {ecoScore && showOffers && (
          <Card variant="outlined">
            <CardContent>
              <Offers points={ecoScore.eco_reward_points} />
            </CardContent>
          </Card>
        )}
      </Container>
    </div>
  );
}

export default App;
