import React from 'react';

export default class EmojiButton extends React.Component {
    constructor(props) {
        super(props);
        // this.state = {
        //     last_button: ''
        // };
    }

    render() {
        return (
            <button type="button" id={`emoji-btn-${this.props.id}`}
                    className="btn btn-default" value={this.props.value}
                    onClick={this.props.clickHandler}>
                {this.props.value}
            </button>
        );
    }
}
