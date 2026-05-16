// this_file: src/mangle.rs

pub struct Mulberry32 {
    state: u32,
}

impl Mulberry32 {
    pub fn new(seed: u64) -> Self {
        let state = (seed ^ (seed >> 32)) as u32;
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

const ROTATION_RULES: [(char, char); 10] = [
    ('c', 'q'),
    ('f', 'v'),
    ('k', 'c'),
    ('q', 'k'),
    ('s', 'z'),
    ('z', 's'),
    ('v', 'f'),
    ('w', 'u'),
    ('b', 'p'),
    ('p', 'b'),
];

const ALL_ROTATIONS: u16 = (1 << ROTATION_RULES.len()) - 1;

pub fn active_rotation_mask(rng: &mut Mulberry32) -> u16 {
    let mut order = [0usize, 1, 2, 3, 4, 5, 6, 7, 8, 9];
    let active_count = rng.range(ROTATION_RULES.len()) + 1;
    for i in 0..active_count {
        let swap = i + rng.range(order.len() - i);
        order.swap(i, swap);
    }
    let mut mask = 0u16;
    for idx in order.iter().take(active_count) {
        mask |= 1 << idx;
    }
    mask
}

fn rotate_char(c: char, active_mask: u16) -> char {
    let lower = c.to_ascii_lowercase();
    for (idx, (src, dst)) in ROTATION_RULES.iter().enumerate() {
        if (active_mask & (1 << idx)) != 0 && lower == *src {
            return if c.is_ascii_uppercase() {
                dst.to_ascii_uppercase()
            } else {
                *dst
            };
        }
    }
    c
}

pub fn mangle(word: &str) -> String {
    mangle_with_mask(word, ALL_ROTATIONS)
}

pub fn mangle_with_mask(word: &str, active_mask: u16) -> String {
    word.chars().map(|c| rotate_char(c, active_mask)).collect()
}
