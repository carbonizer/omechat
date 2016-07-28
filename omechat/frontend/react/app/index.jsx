import React from 'react';
import ReactDOM from 'react-dom';
import 'bootstrap-loader';
import OmechatForm from './components/OmechatForm.jsx';

$(document).ready(() => {
    ReactDOM.render(
        <OmechatForm placeholder="click emojis to enter" />,
        document.getElementById('frontend')
    );
});
