const path = require('path');
const webpack = require('webpack');
const ExtractTextPlugin = require("extract-text-webpack-plugin");

const PATHS = {
    project_root: path.resolve(__dirname, '../..'),
    backend_app_root: path.resolve(__dirname, '..'),
    frontend_root: __dirname,
    app: path.resolve(__dirname, 'react', 'app'),
    node_modules: path.resolve(__dirname, './node_modules'),
    static: path.join(__dirname, '..', 'static'),
    // scss: path.join(__dirname, '..', '..', '..', 'scss')
    scss: path.resolve(__dirname, './scss')
};

module.exports = {
    entry: {
        app: PATHS.app,
        vendor: [
            'jquery',
            'react',
            'react-dom',
            'bootstrap',
            'bootstrap-sass',
            'babel-polyfill',
            'bootstrap-loader'
        ]
    },
    resolve: {
        extensions: ['', '.js', '.jsx']
    },
    output: {
        path: PATHS.static,
        publicPath: '/static/',
        filename: 'bundle.js'
    },
    module: {
        loaders: [
            {
                test: /\.jsx?$/,
                loaders: ['babel?cacheDirectory'],
                include: PATHS.app
            },
            // {
            //     test: /\.css$/,
            //     loaders: ExtractTextPlugin.extract('style-loader', 'css-loader')
            // },
            // {
            //     test: /\.scss$/,
            //     loader: ExtractTextPlugin.extract('style-loader', 'css-loader!sass-loader')
            // },
            {
                test: /\.(woff|woff2)$/,
                loader: "url-loader?name=[path][name].[ext]?[hash]&limit=10000&mimetype=application/font-woff"
            },
            {
                test: /\.(eot|svg|ttf)$/,
                loader: "file-loader?name=[path][name].[ext]?[hash]"
            }
        ]
    },
    plugins: [
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
            'window.jQuery': 'jquery'
        }),
        new webpack.DefinePlugin({
            "process.env": {
                NODE_ENV: JSON.stringify("production")
            }
        }),
        new webpack.optimize.CommonsChunkPlugin({
            name: 'vendor',
            filename: 'vendor.bundle.js',
            minChunks: Infinity
        })
    ]
    // sassLoader: {
    //     includePaths: [PATHS.scss]
    // }
};
