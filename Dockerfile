FROM linuxserver/rdesktop:ubuntu-kde

# install packages
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
    build-essential \
    clang \
    lld \
    libc++-dev \
    libc++abi-dev \
    python3 \
    openjdk-21-jdk \
    tcl \
    zsh \
    curl \
    git \
    stow \
    vim \
    neovim \
    zoxide \
    openssh-server \
    socat \
    ripgrep \
    htop \
    zip

# clean up
RUN apt-get autoclean
RUN rm -rf /config/.cache /var/lib/apt/lists/* /var/tmp/* /tmp/*

# add local files
COPY /root /

# set default shell to zsh
RUN chsh -s /usr/bin/zsh abc

# prepare the config directory
RUN chown -R abc:abc /config

# install bazelisk as bazel
RUN /defaults/install_bazel.sh

# install IDEs
RUN /defaults/install_ide.sh idea 2025.2.1 org.jetbrains.bazel DevKit IdeaVIM
RUN /defaults/install_ide.sh clion 2025.1.5.1 com.google.idea.bazel.clwb IdeaVIM
RUN /defaults/install_ide.sh clion 2025.2.2 com.google.idea.bazel.clwb IdeaVIM

# install JBR 
RUN mkdir -p /opt/jetbrains/jbr
RUN curl -sL "https://cache-redirector.jetbrains.com/intellij-jbr/jbr-21.0.8-linux-aarch64-b1115.48.tar.gz" | tar -xz --strip-components=1 -C /opt/jetbrains/jbr

# clone dotfiles
RUN git clone https://github.com/LeFrosch/dotfiles.git /opt/dotfiles

# configure ssh 
RUN ssh-keygen -A
RUN mkdir /run/sshd
RUN sed -i 's/^#?PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config 
RUN sed -i 's/^#?PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config
RUN echo "AllowUsers abc" >> /etc/ssh/sshd_config                                               

# user configuration...
USER abc

# install default config
RUN cp /defaults/bashrc /config && cp /defaults/startwm.sh /config

# install oh-my-zsh
RUN RUNZSH=no sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
RUN git clone https://github.com/jeffreytse/zsh-vi-mode "$HOME/.oh-my-zsh/plugins/zsh-vi-mode"

# install dotfiles 
RUN rm /config/.zshrc && stow -t /config -d /opt/dotfiles .

# ...and switch back to root 
USER root

# clear tmp, avoids bugs with remdev permission issues
RUN rm -rf /tmp/*

# expose ssh port
EXPOSE 22
