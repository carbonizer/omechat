import React from 'react';
import EmojiButton from './EmojiButton';
import io from 'socket.io-client';

export default class OmechatForm extends React.Component {
    constructor(props) {
        super(props);
        this._handle_click = this._handle_click.bind(this);
        this._handle_reset = this._handle_reset.bind(this);
        this._handle_submit = this._handle_submit.bind(this);
        this.state = {
            messages: [],
            msg: ''
        }
    }

    componentDidMount() {
        this.socket = io(`http://${document.domain}:${location.port}`,
            {path: `${location.pathname}socket.io`});
        this.socket.on('connect', () => {
            console.log(`${this.socket.id}`);
            this.socket.emit('my event', {data: 'I\'m connected'});
        });
        this.socket.on('message', data => {
            this.setState({messages: [data, ...this.state.messages]});
        })
    }

    _handle_submit(e) {
        e.preventDefault();
        console.log(`Going to submit ${JSON.stringify(this.state.msg)}`);
        this.socket.emit('message', this.state.msg, _ => {
            this.setState({msg: ''});
        });
    }

    _handle_reset(e) {
        e.preventDefault();
        console.log('Reset msg');
        this.setState({msg: ''});
    }

    _handle_click(e) {
        e.preventDefault();
        console.log(`Clicked ${e.target.value}`);
        this.setState({'msg': this.state.msg.concat(e.target.value)});
    }

    render() {
        const bound_handle_click = this._handle_click;
        const button_nodes = '😀 😬 😁 😂 😃 😄 😅 😆 😇 😉 😊 🙂 🙃 ☺️ 😋 😌 😍 😘 😗 😙 😚 😜 😝 😛 🤑 🤓 😎 🤗 😏 😶 😐 😑 😒 🙄 🤔 😳 😞 😟 😠 😡 😔 😕 🙁 ☹️ 😣 😖 😫 😩 😤 😮 😱 😨 😰 😯 😦 😧 😢 😥 😪 😓 😭 😵 😲 🤐 😷 🤒 🤕 😴 💤 💩 😈 👿 👹 👺 💀 👻 👽 🤖 😺 😸 😹 😻 😼 😽 🙀 😿 😾 🙌 👏 👋 👍 👊 ✊ ✌️ 👌 ✋ 💪 🙏 ☝️ 👆 👇 👈 👉 🖕 🤘 🖖 ✍️ 💅 👄 👅 👂 👃 👁 👀 👤 🗣 👶 👦 👧 👨 👩 👱 👴 👵 👲 👳 👮 👷 💂 🕵 🎅 👼 👸 👰 🚶 🏃 💃 👯 👫 👬 👭 🙇 💁 🙅 🙆 🙋 🙎 🙍 💇 💆 💑 👩‍❤️‍👩 👨‍❤️‍👨 💏 👩‍❤️‍💋‍👩 👨‍❤️‍💋‍👨 👪 👨‍👩‍👧 👨‍👩‍👧‍👦 👨‍👩‍👦‍👦 👨‍👩‍👧‍👧 👩‍👩‍👦 👩‍👩‍👧 👩‍👩‍👧‍👦 👩‍👩‍👦‍👦 👩‍👩‍👧‍👧 👨‍👨‍👦 👨‍👨‍👧 👨‍👨‍👧‍👦 👨‍👨‍👦‍👦 👨‍👨‍👧‍👧 👚 👕 👖 👔 👗 👙 👘 💄 💋 👣 👠 👡 👢 👞 👟 👒 🎩 ⛑ 🎓 👑 🎒 👝 👛 👜 💼 👓 🕶 💍 🌂'.split(' ')
            .map((emoji) => {
                return (
                    <EmojiButton clickHandler={bound_handle_click}
                                 value={emoji}/>
                );
            });

        const message_nodes = this.state.messages.map(message => {
            return (
                <p><strong>{message.from}:</strong> {message.body}</p>
            );
        });

        return (
            <form id={`omechat-form`}
                  className="omechat-form"
                  onSubmit={this._handle_submit}>
                <div className="row">
                    <div className="col-xs-6 col-md-8">
                        <div className="row">
                            <div className="col-xs-12 input-group">
                                <input id="emoji-text-input"
                                       className="form-control"
                                       aria-label="emoji input" type="text"
                                       readOnly={true}
                                       placeholder={this.props.placeholder}
                                       value={this.state.msg}/>
                                <div className="input-group-btn">
                                    <button className="btn btn-default"
                                            type="submit">
                                        Send
                                    </button>
                                    <button className="btn btn-default"
                                            type="reset"
                                            onClick={this._handle_reset}>
                                        Clear
                                    </button>
                                </div>
                            </div>
                        </div>
                        <br />
                        <div className="row">
                            <div className="col-xs-12">

                                {button_nodes}
                            </div>
                        </div>
                    </div>
                    <div className="col-xs-6 col-md-4">

                        <div>
                            {message_nodes.length ?
                                message_nodes :
                                <em>no messages</em>}
                        </div>
                    </div>
                </div>

            </form>
        );
    }
}
