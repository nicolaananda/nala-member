const VIDEO_ID = /^[A-Za-z0-9_-]{11}$/;
const HOSTS = new Set(['youtube.com', 'www.youtube.com', 'm.youtube.com', 'music.youtube.com', 'youtu.be', 'youtube-nocookie.com', 'www.youtube-nocookie.com']);

export function parseYouTube(value) {
  const input = String(value || '').trim();
  if (!input) return '';
  if (VIDEO_ID.test(input)) return input;
  const raw = input.match(/^https:\/\/([^/?#]+)(\/[^?#]*)?(?:[?#].*)?$/i);
  if (!raw || !HOSTS.has(raw[1].toLowerCase()) || /[\s\\\u0000-\u001f\u007f]/.test(input)) throw Error('Gunakan ID 11 karakter atau tautan HTTPS YouTube yang valid.');
  let url;
  try { url = new URL(input); } catch { throw Error('Gunakan ID 11 karakter atau tautan HTTPS YouTube yang valid.'); }
  if (url.pathname !== (raw[2] || '/')) throw Error('Gunakan ID 11 karakter atau tautan HTTPS YouTube yang valid.');
  let id;
  if (url.hostname === 'youtu.be') id = url.pathname.match(/^\/([\w-]{11})\/?$/)?.[1];
  else if (url.hostname.endsWith('youtube-nocookie.com')) id = url.pathname.match(/^\/embed\/([\w-]{11})\/?$/)?.[1];
  else if (url.pathname === '/watch' && url.searchParams.getAll('v').length === 1) id = url.searchParams.get('v');
  else id = url.pathname.match(/^\/(?:shorts|embed|live)\/([\w-]{11})\/?$/)?.[1];
  if (!id || !VIDEO_ID.test(id)) throw Error('Gunakan ID 11 karakter atau tautan HTTPS YouTube yang valid.');
  return id;
}
