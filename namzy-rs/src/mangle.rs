//! this_file: src/mangle.rs

use crate::wordlist::{ROTATIONS, STEMS};

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

    pub fn coin(&mut self) -> bool {
        (self.next_u32() & 1) == 1
    }
}

fn rotation_for(c: char) -> Option<char> {
    let low = c.to_ascii_lowercase();
    for (src, dst) in ROTATIONS {
        if *src == low {
            return Some(*dst);
        }
    }
    None
}

fn rotate_at(chars: &mut [char], pos: usize) {
    if pos >= chars.len() {
        return;
    }
    let ch = chars[pos];
    if let Some(dst) = rotation_for(ch) {
        chars[pos] = if ch.is_ascii_uppercase() {
            dst.to_ascii_uppercase()
        } else {
            dst
        };
    }
}

pub fn apply_rotations(compound: &str, rng: &mut Mulberry32) -> String {
    let mut chars: Vec<char> = compound.chars().collect();
    if chars.is_empty() {
        return String::new();
    }
    let passes = if rng.coin() { 1 } else { 2 };
    for _ in 0..passes {
        let pos = rng.range(chars.len());
        rotate_at(&mut chars, pos);
    }
    chars.into_iter().collect()
}

fn capitalize(s: &str) -> String {
    let mut c = s.chars();
    match c.next() {
        None => String::new(),
        Some(f) => f.to_uppercase().collect::<String>() + c.as_str(),
    }
}

pub fn build_name(rng: &mut Mulberry32) -> String {
    let a = STEMS[rng.range(STEMS.len())];
    let b = STEMS[rng.range(STEMS.len())];
    let compound = format!("{}{}", a, b);
    capitalize(&apply_rotations(&compound, rng))
}
