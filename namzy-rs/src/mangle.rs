//! this_file: src/mangle.rs

use crate::wordlist::{BAD_SEAMS, ROTATIONS, STEMS};

const MAX_LEN: usize = 12;
const MAX_TRIES: usize = 8;

pub struct Mulberry32 {
    state: u32,
}

impl Mulberry32 {
    pub fn new(seed: u64) -> Self {
        let state = ((seed ^ (seed >> 32)) as u32).wrapping_add(1);
        Self { state }
    }

    pub fn next_u32(&mut self) -> u32 {
        self.state = self.state.wrapping_add(0x6D2B79F5);
        let mut z = self.state;
        z = (z ^ (z >> 15)).wrapping_mul(z | 1);
        z ^= z.wrapping_add((z ^ (z >> 7)).wrapping_mul(z | 61));
        z ^ (z >> 14)
    }

    pub fn range(&mut self, n: usize) -> usize {
        if n == 0 {
            return 0;
        }
        (self.next_u32() as usize) % n
    }
}

fn has_triple_letter(s: &str) -> bool {
    let bytes = s.as_bytes();
    for i in 2..bytes.len() {
        if bytes[i] == bytes[i - 1] && bytes[i] == bytes[i - 2] {
            return true;
        }
    }
    false
}

fn junction_ugly(compound: &str, junction: usize) -> bool {
    let start = junction.saturating_sub(2);
    let end = (junction + 2).min(compound.len());
    let win = &compound[start..end];
    BAD_SEAMS.iter().any(|seam| win.contains(seam))
}

pub fn apply_rotation(s: &str, rng: &mut Mulberry32) -> String {
    let mut matches: Vec<(usize, &'static str, &'static str)> = Vec::new();
    let bytes = s.as_bytes();
    for i in 0..bytes.len() {
        for (src, dst) in ROTATIONS {
            let src_bytes = src.as_bytes();
            if i + src_bytes.len() <= bytes.len() && &bytes[i..i + src_bytes.len()] == src_bytes {
                matches.push((i, *src, *dst));
            }
        }
    }
    if matches.is_empty() {
        return s.to_string();
    }
    let (i, src, dst) = matches[rng.range(matches.len())];
    let mut out = String::with_capacity(s.len() + dst.len());
    out.push_str(&s[..i]);
    out.push_str(dst);
    out.push_str(&s[i + src.len()..]);
    out
}

fn capitalize(s: &str) -> String {
    let mut c = s.chars();
    match c.next() {
        None => String::new(),
        Some(f) => f.to_uppercase().collect::<String>() + c.as_str(),
    }
}

pub fn build_name(rng: &mut Mulberry32) -> String {
    let mut best = String::new();
    for _ in 0..MAX_TRIES {
        let a = STEMS[rng.range(STEMS.len())];
        let b = STEMS[rng.range(STEMS.len())];
        let compound = format!("{}{}", a, b);
        if compound.len() > MAX_LEN
            || has_triple_letter(&compound)
            || junction_ugly(&compound, a.len())
        {
            if best.is_empty() {
                best = compound;
            }
            continue;
        }
        return capitalize(&apply_rotation(&compound, rng));
    }
    capitalize(&apply_rotation(&best, rng))
}
