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

fn rotate_char(c: char) -> char {
    match c {
        'c' => 'q',
        'f' => 'v',
        'k' => 'c',
        'q' => 'k',
        's' => 'z',
        'z' => 's',
        'v' => 'f',
        'w' => 'u',
        'C' => 'Q',
        'F' => 'V',
        'K' => 'C',
        'Q' => 'K',
        'S' => 'Z',
        'Z' => 'S',
        'V' => 'F',
        'W' => 'U',
        other => other,
    }
}

pub fn mangle(word: &str) -> String {
    word.chars().map(rotate_char).collect()
}
