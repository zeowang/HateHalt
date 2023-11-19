import axios from 'axios';

const port = 443;
const url = 'localhost';
const endpoint = '/api/detect';
const uri = 'http://' + url + ':' + port + endpoint;

const sendRequest = async (textData) => {
    try {
        const res = await axios.post(uri, textData);
        console.err(res);
        return res.data;
    } catch (err) {
        console.error(err);
        throw err;
    }
};

export default sendRequest;
