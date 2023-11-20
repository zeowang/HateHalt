import axios from 'axios';

const port = 5000;
const url = 'localhost';
const endpoint = '/api/detect';
const uri = 'http://' + url + ':' + port + endpoint;

const sendRequest = async (textData) => {
    try {
        const json_data = {
            strings: [textData],
        };
        const res = await axios.post(uri, json_data);
        console.log(res);

        return res.data.labels[0];
    } catch (err) {
        console.error(err);
        throw err;
    }
};

export default sendRequest;
