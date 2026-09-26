# Nala Member

Frontend statis Astro untuk portal member Artstudio Nala. Repository ini tidak menyertakan atau mendeploy API/backend.

## Pengembangan

Memerlukan Node.js `^20.19.0 || >=22.12.0`.

```sh
cp .env.example .env
npm ci
npm run dev
```

`PUBLIC_API_URL` adalah URL publik backend yang dikonsumsi frontend. Nilai bawaan aplikasi adalah `https://api.artstudionala.com`; atur variabel ini sesuai lingkungan.

## Cloudflare Pages

- Root directory: `/`
- Build command: `npm run build`
- Build output directory: `dist`
- Environment variable: `PUBLIC_API_URL` dengan URL backend yang sesuai
- Node.js: `^20.19.0 || >=22.12.0`

Deployment frontend tidak mendeploy API dan bukan pernyataan bahwa seluruh sistem siap produksi.
