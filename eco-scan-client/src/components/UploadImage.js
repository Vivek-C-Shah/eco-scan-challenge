import React, { useState } from "react";
import axios from "axios";
import Webcam from "react-webcam";
import {
  Button,
  Typography,
  Box,
  Paper,
  Grid,
  IconButton,
} from "@mui/material";
import { useDropzone } from "react-dropzone";
import DeleteIcon from "@mui/icons-material/Delete";

function UploadImage({ setResults }) {
  const [images, setImages] = useState([]);
  const [imagePreviews, setImagePreviews] = useState([]);
  const [useWebcam, setUseWebcam] = useState(false);
  const webcamRef = React.useRef(null);

  const captureImage = () => {
    const imageSrc = webcamRef.current.getScreenshot();
    fetch(imageSrc)
      .then(res => res.blob())
      .then(blob => {
        const file = new File([blob], "captured-image.jpg", {
          type: "image/jpeg",
        });
        setImages(prevImages => [...prevImages, file]);
        setImagePreviews(prevPreviews => [
          ...prevPreviews,
          URL.createObjectURL(file),
        ]);
      });
  };

  const analyzeImage = async () => {
    if (images.length === 0) return;

    const formData = new FormData();
    images.forEach((image, index) => {
      formData.append("file", image); // Ensure the key is 'file'
    });

    try {
      const response = await axios.post(
        `${process.env.REACT_APP_API_URL}/analyze-image`,
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );
      setResults(prevResults => ({
        identified_items: [
          ...(prevResults?.identified_items || []),
          ...response.data.identified_items,
        ],
        carbon_scores: {
          ...(prevResults?.carbon_scores || {}),
          ...response.data.carbon_scores,
        },
      }));
    } catch (error) {
      console.error(error);
      alert("Error analyzing image");
    }
  };

  const onDrop = acceptedFiles => {
    const newImages = acceptedFiles;
    const newPreviews = newImages.map(file => URL.createObjectURL(file));

    setImages(prevImages => [...prevImages, ...newImages]);
    setImagePreviews(prevPreviews => [...prevPreviews, ...newPreviews]);
  };

  const removeImage = index => {
    const updatedImages = images.filter((_, i) => i !== index);
    const updatedPreviews = imagePreviews.filter((_, i) => i !== index);

    setImages(updatedImages);
    setImagePreviews(updatedPreviews);

    // Reanalyze the remaining images
    if (updatedImages.length > 0) {
      const formData = new FormData();
      updatedImages.forEach((image, idx) => {
        formData.append("file", image);
      });

      axios
        .post(`${process.env.REACT_APP_API_URL}/analyze-image`, formData, {
          headers: { "Content-Type": "multipart/form-data" },
        })
        .then(response => {
          setResults({
            identified_items: response.data.identified_items,
            carbon_scores: response.data.carbon_scores,
          });
        })
        .catch(error => {
          console.error(error);
          alert("Error reanalyzing images");
        });
    } else {
      // If no images are left, clear the results
      setResults({ identified_items: [], carbon_scores: {} });
    }
  };

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    accept: "image/*",
    multiple: true,
  });

  return (
    <Box textAlign="center" marginBottom="2rem">
      <Typography variant="h4" gutterBottom>
        EcoScan - Clothing Carbon Footprint Scanner
      </Typography>

      <Grid container spacing={2} justifyContent="center">
        <Grid item xs={12} sm={6}>
          <Paper
            elevation={3}
            {...getRootProps()}
            style={{ padding: "1rem", cursor: "pointer" }}
          >
            <input {...getInputProps()} />
            <Typography variant="body1">
              Drop images here, or click to select files
            </Typography>
          </Paper>
          {imagePreviews.length > 0 && (
            <Box mt={2} display="flex" flexWrap="wrap" justifyContent="center">
              {imagePreviews.map((preview, index) => (
                <Box
                  key={index}
                  position="relative"
                  display="inline-block"
                  m={1}
                >
                  <img
                    src={preview}
                    alt={`Preview ${index}`}
                    style={{
                      maxWidth: "100px",
                      maxHeight: "100px",
                      display: "block",
                    }}
                  />
                  <IconButton
                    size="small"
                    onClick={() => removeImage(index)}
                    style={{
                      position: "absolute",
                      top: 0,
                      right: 0,
                      backgroundColor: "rgba(255, 255, 255, 0.7)",
                    }}
                  >
                    <DeleteIcon fontSize="small" />
                  </IconButton>
                </Box>
              ))}
            </Box>
          )}
        </Grid>

        <Grid item xs={12} sm={6}>
          {!useWebcam ? (
            <Button
              variant="contained"
              onClick={() => setUseWebcam(true)}
              fullWidth
            >
              Use Camera
            </Button>
          ) : (
            <>
              <Webcam
                audio={false}
                ref={webcamRef}
                screenshotFormat="image/jpeg"
                style={{ margin: "1rem 0" }}
              />
              <Button
                variant="contained"
                onClick={captureImage}
                fullWidth
                style={{ marginBottom: "1rem" }}
              >
                Capture
              </Button>
              <Button
                variant="contained"
                onClick={() => setUseWebcam(false)}
                fullWidth
              >
                Cancel
              </Button>
            </>
          )}
        </Grid>
      </Grid>

      <Button
        variant="contained"
        color="primary"
        onClick={analyzeImage}
        disabled={images.length === 0}
        style={{ marginTop: "1rem" }}
      >
        Analyze Images
      </Button>
    </Box>
  );
}

export default UploadImage;
