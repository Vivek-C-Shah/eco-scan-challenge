// src/components/Offers.js

import React, { useEffect, useState } from "react";
import axios from "axios";
import { Box, Typography, List, ListItem, ListItemText } from "@mui/material";

function Offers({ points }) {
  const [offers, setOffers] = useState([]);

  useEffect(() => {
    const fetchOffers = async () => {
      try {
        const response = await axios.get(`${process.env.REACT_APP_API_URL}/get-offers`, {
          params: { points },
        });
        setOffers(response.data.available_offers);
      } catch (error) {
        console.error(error);
        alert("Error fetching offers");
      }
    };

    if (points > 0) {
      fetchOffers();
    }
  }, [points]);

  if (offers.length === 0) return null;

  return (
    <Box marginTop="2rem">
      <Typography variant="h5" gutterBottom>
        Available Offers:
      </Typography>
      <List>
        {offers.map((offer) => (
          <ListItem key={offer.id}>
            <ListItemText
              primary={offer.offer}
              secondary={`Points Required: ${offer.points_required}`}
            />
          </ListItem>
        ))}
      </List>
    </Box>
  );
}

export default Offers;
