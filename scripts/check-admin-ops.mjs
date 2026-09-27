import assert from 'node:assert/strict';
import { parseYouTube } from '../src/lib/youtube.js';

assert.equal(parseYouTube('dQw4w9WgXcQ'), 'dQw4w9WgXcQ');
assert.equal(parseYouTube('https://youtu.be/dQw4w9WgXcQ?t=2'), 'dQw4w9WgXcQ');
assert.equal(parseYouTube('https://www.youtube.com/watch?v=dQw4w9WgXcQ'), 'dQw4w9WgXcQ');
assert.equal(parseYouTube('https://www.youtube-nocookie.com/embed/dQw4w9WgXcQ'), 'dQw4w9WgXcQ');
for (const value of ['http://youtu.be/dQw4w9WgXcQ', 'https://evil.test/watch?v=dQw4w9WgXcQ', 'https://youtube.com.evil.test/watch?v=dQw4w9WgXcQ', 'too-short']) assert.throws(() => parseYouTube(value));
console.log('admin ops checks passed');
