/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        '../templates/**/*.html',

        '../../templates/**/*.html',

        '../../**/templates/**/*.html',

        '!../../**/node_modules',
        '../../**/*.js',

        '../../**/*.py'
    ],
    theme: {
        extend: {
            colors: {
                'noir-profond': '#0A0A0A',
                'noir-doux':    '#1A1A1A',
                'gris-fonce':   '#2A2A2A',
                'blanc-casse':  '#F5F5F5',
                'or':           '#D4AF37',
                'or-clair':     '#E6C96E',
            },
            fontFamily: {
                'titre':      ['"Bebas Neue"', 'sans-serif'],
                'sous-titre': ['Oswald', 'sans-serif'],
                'texte':      ['Inter', 'sans-serif'],
            },
        },
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
