const axios = require('axios');

const getPudgyPenguinsByTrait = async (traitName, traitValue) => {
    try {
        const response = await axios.get('https://api.opensea.io/api/v1/assets', {
            headers: {
                'X-API-KEY': process.env.OPENSEA_API_KEY, // Add your OpenSea API key here
            },
            params: {
                collection: 'pudgy-penguins',
                [`traits[${traitName}]`]: traitValue,
                limit: 50,
            },
        });

        const penguins = response.data.assets.map((asset) => asset.token_id);
        console.log(`Token IDs with ${traitName}=${traitValue}:`, penguins);
    } catch (error) {
        console.error('Error fetching Pudgy Penguins:', error.response?.data || error.message);
    }
};

getPudgyPenguinsByTrait('Background', 'Blue');
