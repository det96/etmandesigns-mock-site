import fs from 'node:fs'
import path from 'node:path'
import { defineConfig } from 'vite'

const root = path.resolve('.')

function stableAssetName(assetInfo) {
  const name = assetInfo.names?.[0] || assetInfo.name || ''
  if (/\.(?:png|ico|svg|webmanifest)$/i.test(name)) return 'assets/[name][extname]'
  return 'assets/[name]-[hash][extname]'
}

// The source page is a classic script plus a plain stylesheet so it runs from
// file://. Vite still extracts CSS into the production build; this copies the
// same classic script next to those assets and drops module-only tags that
// browsers block when dist/index.html is opened from disk.
function classicScriptForFileProtocol() {
  return {
    name: 'classic-script-for-file-protocol',
    apply: 'build',
    configResolved(config) {
      const warn = config.logger.warn.bind(config.logger)
      config.logger.warn = (msg, options) => {
        if (typeof msg === 'string' && msg.includes('can\'t be bundled without type="module"')) return
        warn(msg, options)
      }
    },
    writeBundle(options) {
      const dir = options.dir ?? path.join(root, 'dist')
      const assetsDir = path.join(dir, 'assets')
      fs.mkdirSync(assetsDir, { recursive: true })
      fs.copyFileSync(path.join(root, 'src/main.js'), path.join(assetsDir, 'main.js'))
    },
    transformIndexHtml: {
      order: 'post',
      handler(html) {
        return html
          .replace(/\s*<link\b[^>]*\brel="modulepreload"[^>]*>/gi, '')
          .replace(/\s*<script\b[^>]*\btype="module"[^>]*>\s*<\/script>/gi, '')
          .replace(/\s+crossorigin(?:="[^"]*")?/gi, '')
          .replace(
            /<script\b[^>]*\bsrc="[^"]*src\/main\.js"[^>]*>\s*<\/script>/i,
            '<script src="./assets/main.js"></script>',
          )
          .replace(
            'content="social/etmandesigns_profile_512.png"',
            'content="./assets/etmandesigns_profile_512.png"',
          )
      },
    },
  }
}

export default defineConfig({
  base: './',
  plugins: [classicScriptForFileProtocol()],
  build: {
    modulePreload: false,
    rolldownOptions: {
      output: {
        assetFileNames: stableAssetName,
      },
    },
  },
  server: {
    host: '0.0.0.0',
    port: 4317,
    strictPort: true,
  },
  preview: {
    host: '0.0.0.0',
    port: 4317,
    strictPort: true,
  },
})
