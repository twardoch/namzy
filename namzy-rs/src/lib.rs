// this_file: src/lib.rs

mod mangle;
mod wordlist;

pub use mangle::Mulberry32;

use std::time::{SystemTime, UNIX_EPOCH};

pub struct Options {
    pub online: bool,
    pub seed: Option<u64>,
}

fn capitalize(s: &str) -> String {
    let mut c = s.chars();
    match c.next() {
        None => String::new(),
        Some(f) => f.to_uppercase().collect::<String>() + c.as_str(),
    }
}

fn default_seed() -> u64 {
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_nanos() as u64
}

fn pick_word(list: &[&str], rng: &mut Mulberry32) -> String {
    list[rng.range(list.len())].to_string()
}

fn is_vowel(c: char) -> bool {
    matches!(c, 'a' | 'e' | 'i' | 'o' | 'u' | 'y')
}

pub fn join_clean(a: &str, b: &str) -> String {
    let head: String = a.to_string();
    let mut tail: String = b.to_string();

    for _ in 0..2 {
        if head.is_empty() || tail.is_empty() {
            break;
        }
        let last = head.chars().last().unwrap();
        let first = tail.chars().next().unwrap();
        if last == first {
            tail = tail[first.len_utf8()..].to_string();
        } else if is_vowel(last) && is_vowel(first) {
            tail = tail[first.len_utf8()..].to_string();
        } else {
            break;
        }
    }

    let mut out = head;
    out.push_str(&tail);
    out
}

fn fetch_online() -> Option<Vec<String>> {
    use std::time::Duration;
    let resp = ureq::get("https://random-word-api.herokuapp.com/word?number=2&length=6")
        .timeout(Duration::from_secs(3))
        .call()
        .ok()?;
    let words: Vec<String> = resp.into_json().ok()?;
    if words.len() >= 2 {
        Some(words)
    } else {
        None
    }
}

pub fn generate(opts: &Options) -> String {
    let seed = opts.seed.unwrap_or_else(default_seed);
    let mut rng = Mulberry32::new(seed);

    let (w1, w2) = if opts.online {
        match fetch_online() {
            Some(words) => (words[0].clone(), words[1].clone()),
            None => (
                pick_word(wordlist::GEO, &mut rng),
                pick_word(wordlist::COMMON, &mut rng),
            ),
        }
    } else {
        (
            pick_word(wordlist::GEO, &mut rng),
            pick_word(wordlist::COMMON, &mut rng),
        )
    };

    let a = w1.to_lowercase();
    let b = w2.to_lowercase();
    let fused = join_clean(&a, &b);
    let rotated = mangle::mangle(&fused);
    capitalize(&rotated)
}
