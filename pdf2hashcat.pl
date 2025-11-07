#!/usr/bin/env perl
#
# pdf2hashcat.pl - Extract password hashes from encrypted PDF files
# Supports all PDF versions (1.4, 1.5, 1.6, 1.7, 1.7 Extension Level 3 and 8)
# For use with hashcat
#
# Usage: perl pdf2hashcat.pl <pdf_file>
#
# Hashcat modes:
#   10400 - PDF 1.1-1.3 (Acrobat 2-4) RC4-40
#   10500 - PDF 1.4-1.6 (Acrobat 5-8) RC4-128
#   10600 - PDF 1.7 Level 3 (Acrobat 9) AES-256
#   10700 - PDF 1.4-1.6 (Acrobat 5-8) RC4-128 (user password)
#   25400 - PDF 1.4-1.6 (Acrobat 5-8) AES-128

use strict;
use warnings;
use Getopt::Long;

my $verbose = 0;
GetOptions('verbose|v' => \$verbose);

if (@ARGV != 1) {
    print "Usage: $0 [-v|--verbose] <pdf_file>\n";
    print "\nExtracts password hash from encrypted PDF for use with hashcat\n";
    print "Supports PDF versions 1.4 through 1.7 (including Extension Levels 3 and 8)\n";
    exit 1;
}

my $pdf_file = $ARGV[0];

unless (-f $pdf_file) {
    die "Error: File '$pdf_file' not found\n";
}

# Read the entire PDF file
open(my $fh, '<:raw', $pdf_file) or die "Cannot open file: $!\n";
my $pdf_content = do { local $/; <$fh> };
close($fh);

# Check if it's a valid PDF
unless ($pdf_content =~ /^%PDF-(\d+\.\d+)/) {
    die "Error: Not a valid PDF file\n";
}

my $pdf_version = $1;
print STDERR "PDF Version: $pdf_version\n" if $verbose;

# Find the Encrypt dictionary
my $encrypt_obj = find_encrypt_object($pdf_content);

unless ($encrypt_obj) {
    die "Error: No encryption found in PDF. File may not be password-protected.\n";
}

print STDERR "Found Encrypt object\n" if $verbose;

# Parse encryption parameters
my %params = parse_encrypt_dict($encrypt_obj, $pdf_content);

# Validate we have the minimum required fields
unless ($params{V} && $params{R}) {
    die "Error: Could not extract encryption version (V) or revision (R)\n";
}

print STDERR "Encryption Algorithm: V=$params{V}, R=$params{R}\n" if $verbose;

# Extract the hash and format for hashcat
my $hash = format_for_hashcat(\%params, $pdf_file);

if ($hash) {
    print "$hash\n";
} else {
    die "Error: Could not generate hash for hashcat\n";
}

# ============================================================================
# Subroutines
# ============================================================================

sub find_encrypt_object {
    my ($content) = @_;

    # Look for /Encrypt reference in trailer or catalog
    if ($content =~ m{/Encrypt\s+(\d+)\s+(\d+)\s+R}s) {
        my ($obj_num, $gen_num) = ($1, $2);
        print STDERR "Encrypt object reference: $obj_num $gen_num R\n" if $verbose;

        # Find the actual object
        if ($content =~ m{$obj_num\s+$gen_num\s+obj\s*<<(.+?)>>\s*(?:stream|endobj)}s) {
            return $1;
        }
    }

    # Fallback: search for /Encrypt dictionary directly
    if ($content =~ m{/Encrypt\s*<<(.+?)>>}s) {
        return $1;
    }

    return undef;
}

sub parse_encrypt_dict {
    my ($encrypt_dict, $full_content) = @_;
    my %params;

    # Extract V (algorithm version)
    if ($encrypt_dict =~ m{/V\s+(\d+)}) {
        $params{V} = $1;
    }

    # Extract R (revision)
    if ($encrypt_dict =~ m{/R\s+(\d+)}) {
        $params{R} = $1;
    }

    # Extract P (permissions)
    if ($encrypt_dict =~ m{/P\s+(-?\d+)}) {
        $params{P} = $1;
    } else {
        $params{P} = -1; # Default
    }

    # Extract Length (key length in bits)
    if ($encrypt_dict =~ m{/Length\s+(\d+)}) {
        $params{Length} = $1;
    } else {
        # Default length based on version
        $params{Length} = ($params{V} && $params{V} >= 2) ? 128 : 40;
    }

    # Extract EncryptMetadata (default is true)
    $params{EncryptMetadata} = 1; # Default
    if ($encrypt_dict =~ m{/EncryptMetadata\s+(true|false)}) {
        $params{EncryptMetadata} = ($1 eq 'true') ? 1 : 0;
    }

    # Extract O string (owner password hash)
    $params{O} = extract_hex_string($encrypt_dict, $full_content, 'O');

    # Extract U string (user password hash)
    $params{U} = extract_hex_string($encrypt_dict, $full_content, 'U');

    # Extract OE string (owner encryption key) - PDF 1.7 Extension Level 3
    $params{OE} = extract_hex_string($encrypt_dict, $full_content, 'OE');

    # Extract UE string (user encryption key) - PDF 1.7 Extension Level 3
    $params{UE} = extract_hex_string($encrypt_dict, $full_content, 'UE');

    # Extract Perms string - PDF 1.7 Extension Level 3
    $params{Perms} = extract_hex_string($encrypt_dict, $full_content, 'Perms');

    # Extract ID from trailer
    if ($full_content =~ m{/ID\s*\[\s*<([0-9a-fA-F]+)>}s) {
        $params{ID} = lc($1);
    } elsif ($full_content =~ m{/ID\s*\[\s*\((.+?)\)}s) {
        $params{ID} = unpack('H*', $1);
    }

    print STDERR "Extracted parameters:\n" if $verbose;
    for my $key (sort keys %params) {
        my $val = $params{$key} // 'undef';
        if ($key =~ /^(O|U|OE|UE|Perms|ID)$/ && defined $params{$key}) {
            print STDERR "  $key: " . substr($val, 0, 32) . "...\n" if $verbose;
        } else {
            print STDERR "  $key: $val\n" if $verbose;
        }
    }

    return %params;
}

sub extract_hex_string {
    my ($encrypt_dict, $full_content, $key) = @_;

    # Try to find the key in the encrypt dictionary
    if ($encrypt_dict =~ m{/$key\s+(\d+)\s+(\d+)\s+R}) {
        # It's a reference to another object
        my ($obj_num, $gen_num) = ($1, $2);
        if ($full_content =~ m{$obj_num\s+$gen_num\s+obj\s*<([0-9a-fA-F]+)>}s) {
            return lc($1);
        }
        if ($full_content =~ m{$obj_num\s+$gen_num\s+obj\s*\((.+?)\)}s) {
            return unpack('H*', $1);
        }
    }

    # Try hex string format <...>
    if ($encrypt_dict =~ m{/$key\s*<([0-9a-fA-F]+)>}) {
        return lc($1);
    }

    # Try literal string format (...)
    if ($encrypt_dict =~ m{/$key\s*\((.+?)\)(?:[^)]*$|[^)])}s) {
        my $str = $1;
        # Handle escaped characters
        $str =~ s/\\([0-7]{3})/chr(oct($1))/eg;
        $str =~ s/\\n/\n/g;
        $str =~ s/\\r/\r/g;
        $str =~ s/\\t/\t/g;
        $str =~ s/\\(.)/\1/g;
        return unpack('H*', $str);
    }

    return undef;
}

sub format_for_hashcat {
    my ($params, $filename) = @_;
    my $V = $params->{V};
    my $R = $params->{R};

    # Determine hashcat mode and format
    my $mode;
    my $hash;

    # PDF 1.7 Extension Level 3 and 8 (AES-256)
    # R=5: Extension Level 3, R=6: Extension Level 8
    if ($R >= 5) {
        $mode = 10600;

        # Format: $pdf$V*R*keylen*P*EncryptMetadata*id_len*id*u_len*u*o_len*o*oe_len*oe*ue_len*ue*perms_len*perms
        my $id = $params->{ID} // '';
        my $u = $params->{U} // '';
        my $o = $params->{O} // '';
        my $oe = $params->{OE} // '';
        my $ue = $params->{UE} // '';
        my $perms = $params->{Perms} // '';

        my $keylen = $params->{Length} // 256;
        my $P = $params->{P} // -1;
        my $em = $params->{EncryptMetadata} // 1;

        # Calculate lengths in bytes (hex string length / 2)
        my $id_len = length($id) / 2;
        my $u_len = length($u) / 2;
        my $o_len = length($o) / 2;
        my $oe_len = length($oe) / 2;
        my $ue_len = length($ue) / 2;
        my $perms_len = length($perms) / 2;

        # For R=5/6, we need at least U and O
        unless ($u && $o) {
            die "Error: Missing required U or O string for PDF 1.7+ encryption\n";
        }

        if ($R == 5) {
            # Extension Level 3 - we need OE, UE, and Perms
            $hash = sprintf('$pdf$%d*%d*%d*%d*%d*%d*%s*%d*%s*%d*%s*%d*%s*%d*%s*%d*%s',
                $V, $R, $keylen, $P, $em,
                $id_len, $id,
                $u_len, $u,
                $o_len, $o,
                $oe_len, $oe,
                $ue_len, $ue,
                $perms_len, $perms
            );
        } else {
            # R=6 (Extension Level 8) uses same format
            $hash = sprintf('$pdf$%d*%d*%d*%d*%d*%d*%s*%d*%s*%d*%s*%d*%s*%d*%s*%d*%s',
                $V, $R, $keylen, $P, $em,
                $id_len, $id,
                $u_len, $u,
                $o_len, $o,
                $oe_len, $oe,
                $ue_len, $ue,
                $perms_len, $perms
            );
        }
    }
    # PDF 1.4-1.6 (Acrobat 5-8) - RC4-128 or AES-128
    elsif ($R == 3 || $R == 4) {
        # Mode 10500 for RC4-128, 25400 for AES-128
        # We'll use 10500 as default, user can try both
        $mode = 10500;

        # Format: $pdf$V*R*keylen*P*EncryptMetadata*id_len*id*u_len*u*o_len*o
        my $id = $params->{ID} // '';
        my $u = $params->{U} // '';
        my $o = $params->{O} // '';

        my $keylen = $params->{Length} // 128;
        my $P = $params->{P} // -1;
        my $em = $params->{EncryptMetadata} // 1;

        unless ($u && $o && $id) {
            die "Error: Missing required encryption parameters (U, O, or ID)\n";
        }

        my $id_len = length($id) / 2;
        my $u_len = length($u) / 2;
        my $o_len = length($o) / 2;

        $hash = sprintf('$pdf$%d*%d*%d*%d*%d*%d*%s*%d*%s*%d*%s',
            $V, $R, $keylen, $P, $em,
            $id_len, $id,
            $u_len, $u,
            $o_len, $o
        );
    }
    # PDF 1.1-1.3 (Acrobat 2-4) - RC4-40
    elsif ($R == 2) {
        $mode = 10400;

        my $id = $params->{ID} // '';
        my $u = $params->{U} // '';
        my $o = $params->{O} // '';

        my $keylen = $params->{Length} // 40;
        my $P = $params->{P} // -1;

        unless ($u && $o && $id) {
            die "Error: Missing required encryption parameters (U, O, or ID)\n";
        }

        my $id_len = length($id) / 2;
        my $u_len = length($u) / 2;
        my $o_len = length($o) / 2;

        $hash = sprintf('$pdf$%d*%d*%d*%d*1*%d*%s*%d*%s*%d*%s',
            $V, $R, $keylen, $P,
            $id_len, $id,
            $u_len, $u,
            $o_len, $o
        );
    }
    else {
        die "Error: Unsupported encryption revision R=$R\n";
    }

    print STDERR "\nHashcat mode: $mode\n" if $verbose;
    print STDERR "Hash format: " . substr($hash, 0, 80) . "...\n" if $verbose;

    return $hash;
}

__END__

=head1 NAME

pdf2hashcat.pl - Extract password hashes from encrypted PDF files for hashcat

=head1 SYNOPSIS

    perl pdf2hashcat.pl [-v|--verbose] <pdf_file>

=head1 DESCRIPTION

This script extracts password hashes from encrypted PDF files and formats them
for use with hashcat password cracker. It supports all major PDF versions:

=over 4

=item * PDF 1.1-1.3 (Acrobat 2-4) - RC4-40 bit (hashcat mode 10400)

=item * PDF 1.4-1.6 (Acrobat 5-8) - RC4-128 bit (hashcat mode 10500)

=item * PDF 1.4-1.6 (Acrobat 5-8) - AES-128 bit (hashcat mode 25400)

=item * PDF 1.7 Level 3 (Acrobat 9-X) - AES-256 bit (hashcat mode 10600)

=item * PDF 1.7 Level 8 (Acrobat XI+) - AES-256 bit (hashcat mode 10600)

=back

=head1 OPTIONS

=over 4

=item B<-v, --verbose>

Enable verbose output with debugging information

=back

=head1 EXAMPLES

    # Extract hash from encrypted PDF
    perl pdf2hashcat.pl document.pdf

    # Use with hashcat to crack the password
    perl pdf2hashcat.pl document.pdf > hash.txt
    hashcat -m 10500 hash.txt wordlist.txt

=head1 USAGE WITH HASHCAT

After extracting the hash, use hashcat with the appropriate mode:

    # For PDF 1.4-1.6 (RC4-128)
    hashcat -m 10500 hash.txt wordlist.txt

    # For PDF 1.4-1.6 (AES-128)
    hashcat -m 25400 hash.txt wordlist.txt

    # For PDF 1.7+ (AES-256)
    hashcat -m 10600 hash.txt wordlist.txt

=head1 AUTHOR

Created for legitimate password recovery and security testing purposes.

=head1 LICENSE

Use responsibly and only on PDFs you own or have explicit permission to test.

=cut
